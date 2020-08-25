from abc import ABC, abstractmethod
import threading
from Queue import Queue
import paho.mqtt.client as paho

class Topic(ABC):
    
    def __init__(self, topic_url, topic_data):
        self.topic_url = topic_url
        self.topic_data = topic_data
        self.client = None


    def connect(self, broker_url, broker_port):
        self.client = paho.Client(self.topic_url, clean_session=True, transport="tcp")
        self.client.on_publish = self.on_publish
        self.client.connect(broker_url, broker_port) 

    @abstractmethod
    def run(self):
        pass

    def disconnect(self):
        self.client.disconnect()

    def on_publish(self, client, userdata, result):
        print("data published \n")
        pass


class TopicAuto(Topic, threading.Thread):

    def __init__(self, topic_url, topic_data, time_interval):
        Topic.__init__(self, topic_url, topic_data)
        threading.Thread.__init__(self, args = (), kwargs = None)
        self.time_interval = time_interval


    


