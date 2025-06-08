from json import JSONDecodeError

from pydantic import ValidationError as PydanticValidationError

from utils.exceptions.simulator_validation_error import SimulatorValidationError


def _format_location_string(loc: str | tuple[str | int, ...]) -> str:
    if not isinstance(loc, (tuple, list)):
        return loc
    path = ""
    for i, x in enumerate(loc):
        if isinstance(x, str):
            path += f".{x}" if i > 0 else x
        else:
            path += f"[{x}]"
    return path


def print_validation_error(error: JSONDecodeError | PydanticValidationError | SimulatorValidationError) -> None:
    if isinstance(error, JSONDecodeError):
        print(f"JSON Decode Error: {error.msg} at line {error.lineno}, column {error.colno}")
        return
    detailed_error_message = f"Settings Validation Error: {error.title}"
    for error_entry in error.errors():
        location = _format_location_string(error_entry["loc"])
        detailed_error_message += "\n\t"
        detailed_error_message += f"- {location}: " if location else ""
        detailed_error_message += error_entry["msg"]
        if error_entry["input"]:
            detailed_error_message += f" (received: {error_entry['input']})"
    print(detailed_error_message)
