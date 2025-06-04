import random

from .data_settings import DataSettings


class DataSettingsBool(DataSettings):
    def generate_initial_value(self):
        return random.choice([True, False])

    def generate_next_value(self):
        return not self.get_old_value()  # can be kept the same according to RETAIN_PROBABILITY
