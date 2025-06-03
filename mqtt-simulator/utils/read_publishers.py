import json
from pathlib import Path

from data_classes import BrokerSettings, ClientSettings
from publisher import Publisher
from topic_data import TopicData, TopicDataBool, TopicDataMathExpression, TopicDataNumber, TopicDataRawValue


def load_topic_data(topic_data_object):
    topic_data: list[TopicData] = []
    for data in topic_data_object:
        data_type = data["TYPE"]
        if data_type == "int" or data_type == "float":
            topic_data.append(TopicDataNumber(data))
        elif data_type == "bool":
            topic_data.append(TopicDataBool(data))
        elif data_type == "raw_values":
            topic_data.append(TopicDataRawValue(data))
        elif data_type == "math_expression":
            topic_data.append(TopicDataMathExpression(data))
        else:
            raise NameError(f"Data TYPE '{data_type}' is unknown")
    return topic_data


def read_client_settings(settings_dict: dict, default: ClientSettings) -> ClientSettings:
    return ClientSettings(
        clean=settings_dict.get("CLEAN_SESSION", default.clean),
        retain=settings_dict.get("RETAIN", default.retain),
        qos=settings_dict.get("QOS", default.qos),
        time_interval=settings_dict.get("TIME_INTERVAL", default.time_interval),
    )


def read_publishers(settings_file: Path, is_verbose: bool) -> list[Publisher]:
    publishers: list[Publisher] = []
    default_client_settings = ClientSettings(clean=True, retain=False, qos=2, time_interval=10)
    with open(settings_file) as json_file:
        config = json.load(json_file)
    broker_settings = BrokerSettings(
        url=config.get("BROKER_URL", "localhost"),
        port=config.get("BROKER_PORT", 1883),
        protocol=config.get("PROTOCOL_VERSION", 4),  # mqtt.MQTTv311
        tls_ca_path=config.get("TLS_CA_PATH", None),
        tls_cert_path=config.get("TLS_CERT_PATH", None),
        tls_key_path=config.get("TLS_KEY_PATH", None),
    )
    broker_client_settings = read_client_settings(config, default=default_client_settings)
    # read each configured topic
    for topic in config["TOPICS"]:
        topic_data_object = topic["DATA"]
        topic_payload_root = topic.get("PAYLOAD_ROOT", {})
        topic_client_settings = read_client_settings(topic, default=broker_client_settings)
        if topic["TYPE"] == "single":
            # create single topic with format: /{PREFIX}
            topic_url = topic["PREFIX"]
            # each topic_url should have different data_settings instances
            topic_data = load_topic_data(topic_data_object)
            publishers.append(
                Publisher(
                    broker_settings,
                    topic_url,
                    topic_data,
                    topic_payload_root,
                    topic_client_settings,
                    is_verbose,
                )
            )
        elif topic["TYPE"] == "multiple":
            # create multiple topics with format: /{PREFIX}/{id}
            for id in range(topic["RANGE_START"], topic["RANGE_END"] + 1):
                topic_url = topic["PREFIX"] + "/" + str(id)
                # each topic_url should have different data_settings instances
                topic_data = load_topic_data(topic_data_object)
                publishers.append(
                    Publisher(
                        broker_settings,
                        topic_url,
                        topic_data,
                        topic_payload_root,
                        topic_client_settings,
                        is_verbose,
                    )
                )
        elif topic["TYPE"] == "list":
            # create multiple topics with format: /{PREFIX}/{item}
            for item in topic["LIST"]:
                topic_url = topic["PREFIX"] + "/" + str(item)
                # each topic_url should have different data_settings instances
                topic_data = load_topic_data(topic_data_object)
                publishers.append(
                    Publisher(
                        broker_settings,
                        topic_url,
                        topic_data,
                        topic_payload_root,
                        topic_client_settings,
                        is_verbose,
                    )
                )
    return publishers
