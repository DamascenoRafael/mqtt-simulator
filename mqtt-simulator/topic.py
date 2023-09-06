import time
import json
import random
import threading
from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt
from expression_evaluator import ExpressionEvaluator

class Topic(ABC):
    def __init__(self, broker_url, broker_port, topic_url, topic_data, protocol, clean_session):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic_url = topic_url
        self.topic_data = topic_data
        self.client = None
        self.protocol = protocol
        self.clean_session = clean_session

    def connect(self):
        self.client = mqtt.Client(self.topic_url, clean_session=True, transport='tcp')
        self.client = mqtt.Client(self.topic_url, protocol=self.protocol, clean_session=self.clean_session)
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker_url, self.broker_port) 
        self.client.loop_start()

    @abstractmethod
    def run(self):
        pass

    def disconnect(self):
        self.client.loop_end()
        self.client.disconnect()

    def on_publish(self, client, userdata, result):
        print(f'[{time.strftime("%H:%M:%S")}] Data published on: {self.topic_url}')


class TopicAuto(Topic, threading.Thread):
    def __init__(self, broker_url, broker_port, topic_url, topic_data, protocol, clean_session, time_interval, qos, retain):
        Topic.__init__(self, broker_url, broker_port, topic_url, topic_data, protocol, clean_session)
        threading.Thread.__init__(self, args = (), kwargs = None)
        self.time_interval = time_interval
        self.old_payload = None
        self.expression_evaluators = {}
        self.qos = qos or 2
        self.retain = retain or False

    def run(self):
        self.connect()
        while True:
            payload = self.generate_payload()
            self.old_payload = payload
            self.client.publish(topic=self.topic_url, payload=json.dumps(payload), qos=self.qos, retain=self.retain) 
            time.sleep(self.time_interval)

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
            index = data.get('MIN_INDEX', 0)
            values = data.get('VALUES', [])
            if len(values) > index:
                return { "index": index, "value": values[0] }
            else:
                return { "index": index }
            
    def generate_next_value(self, data, old_value):
        randN = random.random()
        if randN < data.get('RESET_PROBABILITY', 0):
            return self.generate_initial_value(data)
        if data.get('RESTART_ON_BOUNDARIES', False) and (old_value == data.get('MIN_VALUE', 0) or old_value == data.get('MAX_VALUE', 100)):
            return self.generate_initial_value(data)
        if randN < data.get('RETAIN_PROBABILITY', 0):
            return old_value
        if data['TYPE'] == 'bool':
            return not old_value
        elif data['TYPE'] == 'math_expression':
            return self.expression_evaluators[data['NAME']].evaluate_expression()
        elif data['TYPE'] == 'raw_values':
            values = data.get('VALUES', [])
            minIndex = data.get('MIN_INDEX', 0)
            maxIndex = data.get('MAX_INDEX', len(values) - 1)
            if maxIndex >= len(values):
                maxIndex = len(values) - 1
            index = old_value.get('index', minIndex) + 1
            if data.get('RESTART_ON_BOUNDARIES', False) and (index < minIndex or index > maxIndex):
                return self.generate_initial_value(data)
            elif len(values) > index:
                return { "index": index, "value": values[index] }
            else:
                return old_value
        else:
            # generating value for int or float
            step = random.uniform(0, data['MAX_STEP'])
            step = round(step) if data['TYPE'] == 'int' else step
            increase_probability = data['INCREASE_PROBABILITY'] if 'INCREASE_PROBABILITY' in data else 0.5
            if randN < (1 - increase_probability):
                step *= -1
            return max(old_value + step, data['MIN_VALUE']) if step < 0 else min(old_value + step, data['MAX_VALUE'])

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
