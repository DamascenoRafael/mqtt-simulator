from typing import Literal


class SimulatorValidationError(Exception):
    def __init__(self, title: str, message: str, field: str, value_received: str | None):
        super().__init__(message)
        self.title = title
        self.message = message
        self.field = field
        self.value_received = value_received

    def errors(self) -> list[dict[Literal["msg", "loc", "input"], str]]:
        return [{
            "msg": self.message,
            "loc": self.field,
            "input": str(self.value_received)
        }]
