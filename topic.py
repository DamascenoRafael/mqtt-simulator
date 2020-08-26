from abc import ABC, abstractmethod
import threading
from queue import Queue
import paho.mqtt.client as paho
import time
import json
import random

class Topic(ABC):
    
    def __init__(self, topic_url, topic_data):
        self.topic_url = topic_url
        self.topic_data = topic_data
        self.client = None


    def connect(self, broker_url, broker_port):
        self.client = paho.Client(self.topic_url, clean_session=True, transport="tcp")
        self.client.on_publish = self.on_publish
        self.client.connect(broker_url, broker_port) 
        self.client.loop_start()

    @abstractmethod
    def run(self):
        pass

    def disconnect(self):
        self.client.loop_end()
        self.client.disconnect()

    def on_publish(self, client, userdata, result):
        print("data published \n")
        pass


class TopicAuto(Topic, threading.Thread):

    def __init__(self, topic_url, topic_data, broker_url, broker_port, time_interval):
        Topic.__init__(self, topic_url, topic_data)
        threading.Thread.__init__(self, args = (), kwargs = None)
        self.time_interval = time_interval
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.old_payload = None

    def run(self):
        self.connect(self.broker_url, self.broker_port)
        while True:
            payload = self.generateData()
            self.old_payload = payload
            self.client.publish(topic=self.topic_url, payload=json.dumps(payload), qos=2, retain= False) 
            time.sleep(self.time_interval)

    def generateData(self):
        payload = {}
        
        if self.old_payload == None:
            for data in self.topic_data:
                if data["TYPE"] == "int":
                    payload[data["NAME"]] = random.randint(data["RANGE_START"], data["RANGE_END"])
                else:
                    payload[data["NAME"]] = random.uniform(data["RANGE_START"], data["RANGE_END"])
        else:
            payload = self.old_payload
            for data in self.topic_data:
                if random.random() > .75:
                    continue
                if data["TYPE"] == "int":
                    step = random.randint(data["MAX_STEP"]*-1, data["MAX_STEP"])
                else:
                    step = random.uniform(data["MAX_STEP"]*-1, data["MAX_STEP"])

                payload[data["NAME"]] =  max(payload[data["NAME"]]+step, data["RANGE_START"]) if step < 0 else min(payload[data["NAME"]]+step, data["RANGE_END"])

        return payload

    


