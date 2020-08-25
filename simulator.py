import json
from topic import TopicAuto, TopicManual

class Simulator:
    
    def __init__(self, settings_file):
        
        self.topics = []
        with open(settings_file,'r') as json_file:
            config = json.load(json_file)
            self.broker_url = config["BROKER_URL"]
            self.broker_port = config["BROKER_PORT"]
            for topic in config["TOPICS"]:
                self.topics.append(Topic(topic))


    def run(self):
        for topic in self.topics:
            topic.run(self.broker_url) 

    def stop(self):
        pass    
