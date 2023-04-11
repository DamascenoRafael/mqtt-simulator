import time
import json
import random
import threading
from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt

class Topic(ABC):
    def __init__(self, broker_url, broker_port, topic_url, topic_data):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic_url = topic_url
        self.topic_data = topic_data
        self.client = None

    def connect(self):
        self.client = mqtt.Client(self.topic_url, clean_session=True, transport='tcp')
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
    def __init__(self, broker_url, broker_port, topic_url, topic_data, time_interval):
        Topic.__init__(self, broker_url, broker_port, topic_url, topic_data)
        threading.Thread.__init__(self, args = (), kwargs = None)
        self.time_interval = time_interval
        self.old_payload = None

    def run(self):
        self.connect()
        while True:
            payload = self.generate_payload()
            self.old_payload = payload
            self.client.publish(topic=self.topic_url, payload=json.dumps(payload), qos=2, retain=False) 
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

    def generate_next_value(self, data, old_value):
        if 'RESET_PROBABILITY' in data and random.random() < data['RESET_PROBABILITY']:
            return self.generate_initial_value(data)
        if 'RESTART_ON_BOUNDARIES' in data and data['RESTART_ON_BOUNDARIES'] and (old_value == data['MIN_VALUE'] or old_value == data['MAX_VALUE']):
            return self.generate_initial_value(data)
        if random.random() < data['RETAIN_PROBABILITY']:
            return old_value
        if data['TYPE'] == 'bool':
            return not old_value
        else:
            # generating value for int or float
            step = random.uniform(0, data['MAX_STEP'])
            step = round(step) if data['TYPE'] == 'int' else step
            increase_probability = data['INCREASE_PROBABILITY'] if 'INCREASE_PROBABILITY' in data else 0.5
            if random.random() < (1 - increase_probability):
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
                payload[data['NAME']] = self.generate_next_value(data, payload[data['NAME']])
        return payload
