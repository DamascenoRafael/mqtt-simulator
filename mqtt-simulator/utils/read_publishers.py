import json
from pathlib import Path

from publisher import Publisher
from settings_classes import BrokerSettings, ClientSettings, DataSettingsFactory, TopicSettingsFactory


def read_publishers(settings_file: Path, is_verbose: bool) -> list[Publisher]:
    publishers: list[Publisher] = []
    with open(settings_file, encoding="utf-8") as json_file:
        json_object = json.load(json_file)
    broker_settings = BrokerSettings.model_validate(json_object)
    default_client_settings = ClientSettings(CLEAN_SESSION=True, RETAIN=False, QOS=2, TIME_INTERVAL=10)
    broker_client_settings = ClientSettings.model_validate(json_object).resolve_with_default(
        default=default_client_settings
    )
    # read each configured topic
    for topic_object in json_object.get("TOPICS"):
        client_settings = ClientSettings.model_validate(topic_object).resolve_with_default(
            default=broker_client_settings
        )
        topic_settings = TopicSettingsFactory.create(topic_object)
        topic_data_object = topic_object.get("DATA")
        # read each configured topic URL
        for topic_url in topic_settings.topic_urls():
            # each topic_url should have different DataSettings instances
            topic_data = [DataSettingsFactory.create(data_object) for data_object in topic_data_object]
            publishers.append(
                Publisher(
                    broker_settings,
                    topic_url,
                    topic_data,
                    topic_settings.payload_root,
                    client_settings,
                    is_verbose,
                )
            )
    return publishers
