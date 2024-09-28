from abc import ABC, abstractmethod
from utils import shouldRunWithProbability

class TopicData(ABC):
    def __init__(self, data):
        self.data = data
        self.name = data['NAME']
        self.isActive = True
        self.old_value = None

    def generate_value(self):
        new_value = None
        if self.old_value == None:
            # generate initial data
            if 'INITIAL_VALUE' in self.data:
                new_value = self.data['INITIAL_VALUE']
            else:
                new_value = self.generate_initial_value()
        else:
            # generate next data
            if shouldRunWithProbability(self.data.get('RETAIN_PROBABILITY', 0)):
                new_value = self.old_value
            elif shouldRunWithProbability(self.data.get('RESET_PROBABILITY', 0)):
                new_value = self.generate_initial_value()
            else:
                new_value = self.generate_next_value()
        self.old_value = new_value
        return new_value

    @abstractmethod
    def generate_initial_value(self):
        pass
    
    @abstractmethod
    def generate_next_value(self):
        pass