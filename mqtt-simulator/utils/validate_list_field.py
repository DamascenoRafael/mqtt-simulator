from typing import Any

from utils.exceptions.simulator_validation_error import SimulatorValidationError


def validate_list_field(caller: str, field_name: str, data: Any, allow_empty: bool) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("Internal error: validation data was expected to be a dict")
    if field_name not in data:
        raise SimulatorValidationError(
            title=caller,
            message="Field required",
            field=field_name,
            value_received=str(data)
        )
    field_object = data[field_name]
    if not isinstance(field_object, list):
        raise SimulatorValidationError(
            title=caller,
            message="Input should be a valid list",
            field=field_name,
            value_received=str(field_object)
        )
    if not allow_empty and len(field_object) < 1:
        raise SimulatorValidationError(
            title=caller,
            message="List should have at least 1 item",
            field=field_name,
            value_received=str(field_object)
        )
    return data
