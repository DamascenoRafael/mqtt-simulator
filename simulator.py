import json
from topic import TopicAuto

class Simulator:
    
    def __init__(self, settings_file):
        
        self.topics = []
        with open(settings_file,'r') as json_file:
            config = json.load(json_file)
            self.broker_url = config["BROKER_URL"]
            self.broker_port = config["BROKER_PORT"]
            for topic in config["TOPICS"]:
                for id in range(topic["RANGE_START"], topic["RANGE_END"]+1):
                    topic_url = topic["PREFIX"]+'/'+str(id)
                    self.topics.append(TopicAuto(topic_url,  topic["DATA"], self.broker_url, self.broker_port, topic["TIME_INTERVAL"]))

    def run(self):
        for topic in self.topics:
            print(topic.topic_url)
            topic.start() 

    def stop(self):
        for topic in self.topics:
            topic.stop() 

