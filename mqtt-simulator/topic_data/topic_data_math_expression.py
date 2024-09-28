import math
import random
from .topic_data import TopicData

class TopicDataMathExpression(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.expression_evaluator = None

    def generate_initial_value(self):
        self.expression_evaluator = ExpressionEvaluator(self.data['MATH_EXPRESSION'], self.data['INTERVAL_START'], self.data['INTERVAL_END'], self.data['MIN_DELTA'], self.data['MAX_DELTA'])
        return self.expression_evaluator.get_current_expression_value()

    def generate_next_value(self):
        return self.expression_evaluator.get_next_expression_value()


class ExpressionEvaluator():
    def __init__(self, math_expression, interval_start, interval_end, min_delta, max_delta):
        self._math_expression = self.generate_compiled_expression(math_expression)
        self._interval_start = interval_start
        self._interval_end = interval_end
        self._min_delta = min_delta
        self._max_delta = max_delta
        self._x = interval_start

    def get_current_expression_value(self):
        return self._math_expression(self._x)

    def get_next_expression_value(self):
        if self._x > self._interval_end:
            self._x = self._interval_start
            return self.get_current_expression_value()
        step = random.uniform(self._min_delta, self._max_delta)
        self._x += step
        return self.get_current_expression_value()

    def generate_compiled_expression(self, expression):
        lambda_expression = "lambda x: "+expression
        code = compile(lambda_expression, "<string>", "eval")
        ALLOWED_FUNCTIONS = {function_name: func for function_name, func in math.__dict__.items() if not function_name.startswith("__")}
        for name in code.co_names:
            if name not in ALLOWED_FUNCTIONS:
                raise NameError(f"The use of '{name}' is not allowed")
        return eval(code, {"__builtins__": {}, "math":math}, ALLOWED_FUNCTIONS)
