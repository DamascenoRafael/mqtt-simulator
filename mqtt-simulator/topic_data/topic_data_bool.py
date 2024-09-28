import random
from .topic_data import TopicData

class TopicDataBool(TopicData):
    def __init__(self, data):
        super().__init__(data)

    def generate_initial_value(self):
        return random.choice([True, False])

    def generate_next_value(self):
        return not self.old_value # can be kept the same according to RETAIN_PROBABILITY
