from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr
from utils.should_run_with_probability import should_run_with_probability


class DataSettings(ABC, BaseModel):
    type: str = Field(alias="TYPE")
    name: str = Field(alias="NAME")
    initial_value: Any = Field(alias="INITIAL_VALUE", default=None)
    retain_probability: float = Field(alias="RETAIN_PROBABILITY", default=0.0)
    reset_probability: float = Field(alias="RESET_PROBABILITY", default=0.0)
    _is_active: bool = PrivateAttr(default=True)
    _old_value: Any = PrivateAttr(default=None)

    def get_is_active(self) -> bool:
        return self._is_active

    def set_is_active(self, is_active: bool) -> None:
        self._is_active = is_active

    def get_old_value(self) -> Any:
        return self._old_value

    def generate_value(self) -> Any:
        new_value = None
        if self._old_value is None:
            # generate initial data
            if self.initial_value is not None:
                new_value = self.initial_value
            else:
                new_value = self.generate_initial_value()
        else:
            # generate next data
            if should_run_with_probability(self.retain_probability):
                new_value = self._old_value
            elif should_run_with_probability(self.reset_probability):
                new_value = self.generate_initial_value()
            else:
                new_value = self.generate_next_value()
        self._old_value = new_value
        return new_value

    @abstractmethod
    def generate_initial_value(self) -> Any:
        pass

    @abstractmethod
    def generate_next_value(self) -> Any:
        pass
