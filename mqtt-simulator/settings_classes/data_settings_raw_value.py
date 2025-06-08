from typing import Any

from pydantic import Field, PrivateAttr

from .data_settings import DataSettings


class DataSettingsRawValue(DataSettings):
    restart_on_end: bool = Field(alias="RESTART_ON_END", default=False)
    values: list[Any] = Field(alias="VALUES", min_length=1)
    value_default: dict[str, Any] | None = Field(alias="VALUE_DEFAULT", default=None)
    index_start: int = Field(alias="INDEX_START", default=0)
    index_end: int = Field(alias="INDEX_END", default_factory=lambda dict: len(dict.get("values", [])) - 1)

    _raw_values_index: int = PrivateAttr(default=0)

    def generate_initial_value(self):
        self._raw_values_index = self.index_start
        return self.get_current_value()

    def generate_next_value(self):
        self._raw_values_index += 1
        if self._raw_values_index <= self.index_end:
            return self.get_current_value()
        elif self._raw_values_index > self.index_end and self.restart_on_end:
            return self.generate_initial_value()
        else:
            # changing to not active, if all data within the topic is not active we can disconnect the topic
            self.set_is_active(False)
            return None

    def get_current_value(self) -> Any:
        current_value_for_index = self.values[self._raw_values_index]
        if self.value_default is not None:
            # raw_value needs to be of type dict/object
            value: dict[str, Any] = {}
            value.update(self.value_default)
            value.update(current_value_for_index)
            return value
        # raw_value can be of any type
        return current_value_for_index
