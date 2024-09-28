from .topic_data import TopicData

class TopicDataRawValue(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.raw_values_index = 0

    def generate_initial_value(self):
        self.raw_values_index = self.data.get('INDEX_START', 0)
        return self.get_current_value()

    def generate_next_value(self):
        end_index = self.data.get('INDEX_END', len(self.data['VALUES']) - 1)
        self.raw_values_index += 1
        if self.raw_values_index <= end_index:
            return self.get_current_value()
        elif self.raw_values_index > end_index and self.data.get('RESTART_ON_END', False):
            return self.generate_initial_value()
        else:
            # changing to not active, if all data within the topic is not active we can disconnect the topic
            self.is_active = False

    def get_current_value(self):
        current_value_for_index = self.data['VALUES'][self.raw_values_index]
        if 'VALUE_DEFAULT' in self.data:
            # raw_value needs to be of type object
            value = {}
            value.update(self.data.get('VALUE_DEFAULT', {}))
            value.update(current_value_for_index)
            return value
        # raw_value can be of any type
        return current_value_for_index
