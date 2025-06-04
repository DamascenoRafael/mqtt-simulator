from typing import Any


def validate_list_field(field_name: str, data: Any, allow_empty: bool) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("Internal error: validation data was expected to be a dict")
    if field_name not in data:
        raise ValueError(f"'{field_name}' must be included")
    field_object = data[field_name]
    if not isinstance(field_object, list):
        raise ValueError(f"'{field_name}' must be a list")
    if not allow_empty and len(field_object) < 1:
        raise ValueError(f"'{field_name}' must have at least one item")
    return data
