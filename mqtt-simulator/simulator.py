import json
from pathlib import Path
from topic import Topic
from data_classes import BrokerSettings, ClientSettings

class Simulator:
    def __init__(self, settings_file: Path):
        self.topics = self.load_topics(settings_file)

    def read_client_settings(self, settings_dict: dict, default: ClientSettings) -> ClientSettings:
        return ClientSettings(
            clean=settings_dict.get("CLEAN_SESSION", default.clean),
            retain=settings_dict.get("RETAIN", default.retain),
            qos=settings_dict.get("QOS", default.qos),
            time_interval=settings_dict.get("TIME_INTERVAL", default.time_interval),
        )

    def load_topics(self, settings_file: Path) -> list[Topic]:
        topics: list[Topic] = []
        default_client_settings = ClientSettings(clean=True, retain=False, qos=2, time_interval=10)
        with open(settings_file) as json_file:
            config = json.load(json_file)
        broker_settings = BrokerSettings(
            url=config.get("BROKER_URL", "localhost"),
            port=config.get("BROKER_PORT", 1883),
            protocol=config.get("PROTOCOL_VERSION", 4), # mqtt.MQTTv311
            tls_ca_path=config.get("TLS_CA_PATH", None),
            tls_cert_path=config.get("TLS_CERT_PATH", None),
            tls_key_path=config.get("TLS_KEY_PATH", None),
        )
        broker_client_settings = self.read_client_settings(config, default=default_client_settings)
        # read each configured topic
        for topic in config["TOPICS"]:
            topic_data = topic["DATA"]
            topic_payload_root = topic.get("PAYLOAD_ROOT", {})
            topic_client_settings = self.read_client_settings(topic, default=broker_client_settings)
            if topic["TYPE"] == "single":
                # create single topic with format: /{PREFIX}
                topic_url = topic["PREFIX"]
                topics.append(
                    Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings)
                )
            elif topic["TYPE"] == "multiple":
                # create multiple topics with format: /{PREFIX}/{id}
                for id in range(topic["RANGE_START"], topic["RANGE_END"] + 1):
                    topic_url = topic["PREFIX"] + "/" + str(id)
                    topics.append(
                        Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings)
                    )
            elif topic["TYPE"] == "list":
                # create multiple topics with format: /{PREFIX}/{item}
                for item in topic["LIST"]:
                    topic_url = topic["PREFIX"] + "/" + str(item)
                    topics.append(
                        Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings)
                    )
        return topics

    def run(self):
        for topic in self.topics:
            print(f"Starting: {topic.topic_url} ...")
            topic.start()

    def stop(self):
        for topic in self.topics:
            print(f"Stopping: {topic.topic_url} ...")
            topic.stop()
