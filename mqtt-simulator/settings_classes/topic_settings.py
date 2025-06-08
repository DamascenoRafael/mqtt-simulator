from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field, model_validator
from utils.validate_list_field import validate_list_field


class TopicSettings(ABC, BaseModel):
    prefix: str = Field(alias="PREFIX")
    payload_root: dict[str, Any] = Field(alias="PAYLOAD_ROOT", default_factory=dict)

    @abstractmethod
    def topic_urls(self) -> list[str]:
        pass

    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, data: Any) -> Any:
        return validate_list_field(caller="TopicSettings", field_name="DATA", data=data, allow_empty=False)


class TopicSingleSettings(TopicSettings):
    # create single topic with format: /{PREFIX}
    def topic_urls(self) -> list[str]:
        return [self.prefix]


class TopicMultipleSettings(TopicSettings):
    range_start: int = Field(alias="RANGE_START")
    range_end: int = Field(alias="RANGE_END")

    # create multiple topics with format: /{PREFIX}/{id}
    def topic_urls(self) -> list[str]:
        return [f"{self.prefix}/{i}" for i in range(self.range_start, self.range_end + 1)]


class TopicListSettings(TopicSettings):
    list_items: list[str | int] = Field(alias="LIST")

    # create multiple topics with format: /{PREFIX}/{item}
    def topic_urls(self) -> list[str]:
        return [f"{self.prefix}/{item}" for item in self.list_items]
