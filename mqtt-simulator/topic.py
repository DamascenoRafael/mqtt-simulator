import time
import json
import random
import threading
from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt
from client_settings import ClientSettings
from expression_evaluator import ExpressionEvaluator

class Topic(ABC):
    def __init__(self, broker_url: str, broker_port: int, broker_protocol: int, topic_url: str, topic_data: list[object], topic_client_settings: ClientSettings):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.broker_protocol = broker_protocol

        self.topic_url = topic_url
        self.topic_data = topic_data
        self.topic_client_settings = topic_client_settings

        self.loop = False
        self.client = None
        self.old_payload = None

    @abstractmethod
    def generate_initial_value(self, data):
        pass
    
    @abstractmethod
    def generate_next_value(self, data, old_value):
        pass

    def connect(self):
        self.loop = True
        if self.broker_protocol == mqtt.MQTTv5:
            self.client = mqtt.Client(self.topic_url, protocol=self.broker_protocol)
        else:
            self.client = mqtt.Client(self.topic_url, protocol=self.broker_protocol, clean_session=self.topic_client_settings.clean)
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()

    def disconnect(self):
        self.loop = False
        self.client.loop_stop()
        self.client.disconnect()

    def run(self):
        self.connect()
        while self.loop:
            payload = self.generate_payload()
            self.old_payload = payload
            self.client.publish(topic=self.topic_url, payload=json.dumps(payload), qos=self.topic_client_settings.qos, retain=self.topic_client_settings.retain)
            time.sleep(self.topic_client_settings.time_interval)

    def on_publish(self, client, userdata, result):
        print(f'[{time.strftime("%H:%M:%S")}] Data published on: {self.topic_url}')

    def generate_payload(self):
        payload = {}
        if self.old_payload == None:
            # generate initial data
            for data in self.topic_data:
                payload[data['NAME']] = self.generate_initial_value(data)
        else:
            # generate next data
            for data in self.topic_data:
                payload[data['NAME']] = self.generate_next_value(data, self.old_payload[data['NAME']])
        return payload


class TopicAuto(Topic, threading.Thread):
    def __init__(self, broker_url: str, broker_port: int, broker_protocol: int, topic_url: str, topic_data: list[object], topic_client_settings: ClientSettings):
        Topic.__init__(self, broker_url, broker_port, broker_protocol, topic_url, topic_data, topic_client_settings)
        threading.Thread.__init__(self, args = (), kwargs = None)

        # Relevant for when TYPE is 'math_expression'
        self.expression_evaluators = {}

        # Relevant for when TYPE is 'raw_values'
        self.raw_values_index = 0

    def generate_initial_value(self, data):
        if 'INITIAL_VALUE' in data:
            return data['INITIAL_VALUE']
        elif data['TYPE'] == 'int':
            return random.randint(data['MIN_VALUE'], data['MAX_VALUE'])
        elif data['TYPE'] == 'float':
            return random.uniform(data['MIN_VALUE'], data['MAX_VALUE'])
        elif data['TYPE'] == 'bool':
            return random.choice([True, False])
        elif data['TYPE'] == 'math_expression':
            self.expression_evaluators[data['NAME']] = ExpressionEvaluator(data['MATH_EXPRESSION'], data['INTERVAL_START'], data['INTERVAL_END'], data['MIN_DELTA'], data['MAX_DELTA'])
            return self.expression_evaluators[data['NAME']].get_current_expression_value()
        elif data['TYPE'] == 'raw_values':
            self.raw_values_index = data.get('INDEX_START', 0)
            values = data['VALUES']
            return values[self.raw_values_index]
            
    def generate_next_value(self, data, old_value):
        randN = random.random()
        if randN < data.get('RESET_PROBABILITY', 0):
            return self.generate_initial_value(data)
        if data.get('RESTART_ON_BOUNDARIES', False) and (old_value == data.get('MIN_VALUE') or old_value == data.get('MAX_VALUE')):
            return self.generate_initial_value(data)
        if randN < data.get('RETAIN_PROBABILITY', 0):
            return old_value
        if data['TYPE'] == 'bool':
            return not old_value
        elif data['TYPE'] == 'math_expression':
            return self.expression_evaluators[data['NAME']].evaluate_expression()
        elif data['TYPE'] == 'raw_values':
            # iterate the raw_values then restart, return next, or disconnect at the end_index
            values = data['VALUES']
            end_index = data.get('INDEX_END', len(values) - 1)
            self.raw_values_index += 1
            if data.get('RESTART_ON_END', False) and self.raw_values_index > end_index:
                return self.generate_initial_value(data)
            elif self.raw_values_index <= end_index:
                return values[self.raw_values_index]
            else:
                self.disconnect()
        else:
            # generating value for int or float
            step = random.uniform(0, data['MAX_STEP'])
            step = round(step) if data['TYPE'] == 'int' else step
            increase_probability = data['INCREASE_PROBABILITY'] if 'INCREASE_PROBABILITY' in data else 0.5
            if randN < (1 - increase_probability):
                step *= -1
            return max(old_value + step, data['MIN_VALUE']) if step < 0 else min(old_value + step, data['MAX_VALUE'])
