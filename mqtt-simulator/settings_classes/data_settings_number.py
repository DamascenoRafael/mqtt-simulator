import random

from pydantic import Field, computed_field
from utils.should_run_with_probability import should_run_with_probability

from .data_settings import DataSettings


class DataSettingsNumber(DataSettings):
    min_value: int | float = Field(alias="MIN_VALUE")
    max_value: int | float = Field(alias="MAX_VALUE")
    max_step: int | float = Field(alias="MAX_STEP")
    increase_probability: float = Field(alias="INCREASE_PROBABILITY", default=0.5)
    restart_on_boundaries: bool = Field(alias="RESTART_ON_BOUNDARIES", default=False)

    @computed_field
    @property
    def is_int(self) -> bool:
        return self.type == "INT"

    def is_old_value_on_boundary(self) -> bool:
        return self.get_old_value() == self.min_value or self.get_old_value() == self.max_value

    def generate_initial_value(self):
        if self.is_int:
            # int number
            return random.randint(int(self.min_value), int(self.max_value))
        else:
            # float number
            return random.uniform(self.min_value, self.max_value)

    def generate_next_value(self):
        if self.restart_on_boundaries and self.is_old_value_on_boundary():
            return self.generate_initial_value()
        step = random.uniform(0, self.max_step)
        step = round(step) if self.is_int else step
        if should_run_with_probability(1 - self.increase_probability):
            step *= -1
        return (
            max(self.get_old_value() + step, self.min_value)
            if step < 0
            else min(self.get_old_value() + step, self.max_value)
        )
