class SimulatorValidationError(Exception):
    def __init__(self, title: str, message: str, field: str, value_received: str | None):
        super().__init__(message)
        self.title = title
        self.message = message
        self.field = field
        self.value_received = value_received
