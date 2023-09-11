import json
from client_settings import ClientSettings
from topic import TopicAuto

class Simulator:
    def __init__(self, settings_file):
        self.topics = []
        self.default_client_settings = ClientSettings(
            clean=True,
            retain=False,
            qos=2,
            time_interval=10
        )
        self.load_topics(settings_file)

    def read_client_settings(self, settings_dict: dict, default: ClientSettings):
        return ClientSettings(
            clean=settings_dict.get('CLEAN_SESSION', default.clean),
            retain=settings_dict.get('RETAIN', default.retain),
            qos=settings_dict.get('QOS', default.qos),
            time_interval= settings_dict.get('TIME_INTERVAL', default.time_interval)
        )

    def load_topics(self, settings_file):
        with open(settings_file) as json_file:
            config = json.load(json_file)
            broker_url = config.get('BROKER_URL', 'localhost')
            broker_port = config.get('BROKER_PORT', 1883)
            broker_protocol = config.get('PROTOCOL_VERSION', 4) # mqtt.MQTTv311
            broker_client_settings = self.read_client_settings(config, default=self.default_client_settings)
            # read each configured topic
            for topic in config['TOPICS']:
                topic_data = topic['DATA']
                topic_client_settings = self.read_client_settings(topic, default=broker_client_settings)
                if topic['TYPE'] == 'single':
                    # create single topic with format: /{PREFIX}
                    topic_url = topic['PREFIX']
                    self.topics.append(TopicAuto(broker_url, broker_port, broker_protocol, topic_url, topic_data, topic_client_settings))
                elif topic['TYPE'] == 'multiple':
                    # create multiple topics with format: /{PREFIX}/{id}
                    for id in range(topic['RANGE_START'], topic['RANGE_END']+1):
                        topic_url = topic['PREFIX'] + '/' + str(id)
                        self.topics.append(TopicAuto(broker_url, broker_port, broker_protocol, topic_url, topic_data, topic_client_settings))
                elif topic['TYPE'] == 'list':
                    # create multiple topics with format: /{PREFIX}/{item}
                    for item in topic['LIST']:
                        topic_url = topic['PREFIX'] + '/' + str(item)
                        self.topics.append(TopicAuto(broker_url, broker_port, broker_protocol, topic_url, topic_data, topic_client_settings))

    def run(self):
        for topic in self.topics:
            print(f'Starting: {topic.topic_url} ...')
            topic.start() 

    def stop(self):
        for topic in self.topics:
            print(f'Stopping: {topic.topic_url} ...')
            topic.stop() 
