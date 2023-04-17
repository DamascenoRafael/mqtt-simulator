import math
import random


class ExpressionEvaluator():
    def __init__(self, math_expression, interval_start, interval_end, min_delta, max_delta):
        self._math_expression = self.generate_compiled_expression(math_expression)
        self._interval_start = interval_start
        self._interval_end = interval_end
        self._min_delta = min_delta
        self._max_delta = max_delta
        self._x = interval_start
    
    def evaluate_expression(self):
        if self._x > self._interval_end:
            self._x = self._interval_start
            return self.get_current_expression_value()
        step = random.uniform(self._min_delta, self._max_delta) 
        self._x += step
        return self.get_current_expression_value()

    def get_current_expression_value(self):
        return self._math_expression(self._x)
    
    def generate_compiled_expression(self, expression):
        lambda_expression = "lambda x: "+expression
        code = compile(lambda_expression, "<string>", "eval")
        ALLOWED_FUNCTIONS = {function_name: func for function_name, func in math.__dict__.items() if not function_name.startswith("__")}

        for name in code.co_names:
            if name not in ALLOWED_FUNCTIONS:
                raise NameError(f"The use of '{name}' is not allowed")
        return eval(code, {"__builtins__": {}, "math":math}, ALLOWED_FUNCTIONS)
