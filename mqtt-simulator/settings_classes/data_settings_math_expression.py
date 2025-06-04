import math
import random

from pydantic import Field, PrivateAttr

from .data_settings import DataSettings


class DataSettingsMathExpression(DataSettings):
    math_expression: str = Field(alias="MATH_EXPRESSION")
    interval_start: int | float = Field(alias="INTERVAL_START")
    interval_end: int | float = Field(alias="INTERVAL_END")
    min_delta: int | float = Field(alias="MIN_DELTA")
    max_delta: int | float = Field(alias="MAX_DELTA")

    _expression_evaluator: "ExpressionEvaluator" = PrivateAttr()

    def generate_initial_value(self):
        self._expression_evaluator = ExpressionEvaluator(
            self.math_expression,
            self.interval_start,
            self.interval_end,
            self.min_delta,
            self.max_delta,
        )
        return self._expression_evaluator.get_current_expression_value()

    def generate_next_value(self):
        return self._expression_evaluator.get_next_expression_value()


class ExpressionEvaluator:
    def __init__(
        self,
        math_expression: str,
        interval_start: int | float,
        interval_end: int | float,
        min_delta: int | float,
        max_delta: int | float,
    ):
        self._math_expression = self.generate_compiled_expression(math_expression)
        self._interval_start = interval_start
        self._interval_end = interval_end
        self._min_delta = min_delta
        self._max_delta = max_delta
        self._x = interval_start

    def get_current_expression_value(self) -> int | float:
        return self._math_expression(self._x)

    def get_next_expression_value(self) -> int | float:
        if self._x > self._interval_end:
            self._x = self._interval_start
            return self.get_current_expression_value()
        step = random.uniform(self._min_delta, self._max_delta)
        self._x += step
        return self.get_current_expression_value()

    def generate_compiled_expression(self, expression: str):
        lambda_expression = "lambda x: " + expression
        code = compile(lambda_expression, "<string>", "eval")
        ALLOWED_FUNCTIONS = {
            function_name: func for function_name, func in math.__dict__.items() if not function_name.startswith("__")
        }
        for name in code.co_names:
            if name not in ALLOWED_FUNCTIONS:
                raise NameError(f"The use of '{name}' is not allowed")
        return eval(code, {"__builtins__": {}, "math": math}, ALLOWED_FUNCTIONS)
