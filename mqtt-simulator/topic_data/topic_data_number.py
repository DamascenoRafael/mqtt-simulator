import random
from .topic_data import TopicData
from utils import shouldRunWithProbability

class TopicDataNumber(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.isInt = data['TYPE'] == 'int'
    
    def generate_initial_value(self):
        if self.isInt:
            # int number
            return random.randint(self.data['MIN_VALUE'], self.data['MAX_VALUE'])
        else: 
            # float number
            return random.uniform(self.data['MIN_VALUE'], self.data['MAX_VALUE'])
        
    def generate_next_value(self):
        if self.data.get('RESTART_ON_BOUNDARIES', False) and (self.old_value == self.data.get('MIN_VALUE') or self.old_value == self.data.get('MAX_VALUE')):
            return self.generate_initial_value()
        step = random.uniform(0, self.data['MAX_STEP'])
        step = round(step) if self.isInt else step
        increase_probability = self.data['INCREASE_PROBABILITY'] if 'INCREASE_PROBABILITY' in self.data else 0.5
        if shouldRunWithProbability(1 - increase_probability):
            step *= -1
        return max(self.old_value + step, self.data['MIN_VALUE']) if step < 0 else min(self.old_value + step, self.data['MAX_VALUE'])
