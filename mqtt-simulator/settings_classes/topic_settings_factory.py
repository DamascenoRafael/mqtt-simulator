from typing import Any, Type

from utils.exceptions.simulator_validation_error import SimulatorValidationError

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
            expected_types = ", ".join(cls._topic_types.keys())
            raise SimulatorValidationError(
                title="TopicSettingsFactory",
                message=f"Input should be a valid topic type, expected one of: {expected_types}",
                field="TYPE",
                value_received=topic_type,
            )
        return cls._topic_types[topic_type].model_validate(data)
