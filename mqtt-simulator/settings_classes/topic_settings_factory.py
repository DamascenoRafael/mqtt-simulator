from typing import Any, Type

from settings_classes.topic_settings import TopicListSettings, TopicMultipleSettings, TopicSettings, TopicSingleSettings


class TopicSettingsFactory:
    _topic_types: dict[str, Type[TopicSettings]] = {
        "single": TopicSingleSettings,
        "multiple": TopicMultipleSettings,
        "list": TopicListSettings,
    }

    @classmethod
    def create(cls, data: dict[str, Any]) -> TopicSettings:
        topic_type = data.get("TYPE")
        if topic_type not in cls._topic_types:
            raise ValueError(f"Invalid TOPIC type: {topic_type}")
        return cls._topic_types[topic_type].model_validate(data)
