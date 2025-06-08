from typing import Any

from utils.exceptions.simulator_validation_error import SimulatorValidationError

from settings_classes.data_settings import DataSettings
from settings_classes.data_settings_bool import DataSettingsBool
from settings_classes.data_settings_math_expression import DataSettingsMathExpression
from settings_classes.data_settings_number import DataSettingsNumber
from settings_classes.data_settings_raw_value import DataSettingsRawValue


class DataSettingsFactory:
    _data_types: dict[str, type[DataSettings]] = {
        "int": DataSettingsNumber,
        "float": DataSettingsNumber,
        "bool": DataSettingsBool,
        "math_expression": DataSettingsMathExpression,
        "raw_values": DataSettingsRawValue,
    }

    @classmethod
    def create(cls, data: dict[str, Any]) -> DataSettings:
        data_type = data.get("TYPE")
        if data_type not in cls._data_types:
            expected_types = ", ".join(cls._data_types.keys())
            raise SimulatorValidationError(
                title="DataSettingsFactory",
                message=f"Input should be a valid data type, expected one of: {expected_types}",
                field="TYPE",
                value_received=data_type,
            )
        return cls._data_types[data_type].model_validate(data)
