import json
from topic import TopicAuto

class Simulator:
    def __init__(self, settings_file):
        self.broker_url = None
        self.broker_port = None
        self.topics = []
        self.load_settings(settings_file)

    def load_settings(self, settings_file):
        with open(settings_file) as json_file:
            config = json.load(json_file)
            self.broker_url = config.get('BROKER_URL', 'localhost')
            self.broker_port = config.get('BROKER_PORT', 1883)
            broker_time_interval = config.get('TIME_INTERVAL', 10)
            broker_protocol = config.get('PROTOCOL_VERSION', 4) # mqtt.MQTTv311
            broker_clean = config.get('CLEAN_SESSION', True)
            broker_qos = config.get('QOS', 2)
            broker_retained = config.get('RETAINED', False)
            # read each configured topic
            for topic in config['TOPICS']:
                topic_data = topic['DATA']
                topic_time_interval = topic.get('TIME_INTERVAL', broker_time_interval)
                topic_protocol = topic.get('PROTOCOL_VERSION', broker_protocol)
                topic_clean = topic.get('CLEAN_SESSION', broker_clean)
                topic_qos = topic.get('QOS', broker_qos)
                topic_retained = topic.get('RETAINED', broker_retained)
                if topic['TYPE'] == 'single':
                    # create single topic with format: /{PREFIX}
                    topic_url = topic['PREFIX']
                    self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_protocol, topic_clean, topic_time_interval, topic_qos, topic_retained))
                elif topic['TYPE'] == 'multiple':
                    # create multiple topics with format: /{PREFIX}/{id}
                    for id in range(topic['RANGE_START'], topic['RANGE_END']+1):
                        topic_url = topic['PREFIX'] + '/' + str(id)
                        self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_protocol, topic_clean, topic_time_interval, topic_qos, topic_retained))
                elif topic['TYPE'] == 'list':
                    # create multiple topics with format: /{PREFIX}/{item}
                    for item in topic['LIST']:
                        topic_url = topic['PREFIX'] + '/' + str(item)
                        self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_protocol, topic_clean, topic_time_interval, topic_qos, topic_retained))
                    

    def run(self):
        for topic in self.topics:
            print(f'Starting: {topic.topic_url} ...')
            topic.start() 

    def stop(self):
        for topic in self.topics:
            print(f'Stopping: {topic.topic_url} ...')
            topic.stop() 
