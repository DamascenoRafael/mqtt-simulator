from __future__ import annotations

from pydantic import BaseModel, Field


class ClientSettingsPartial(BaseModel):
    clean_session: bool | None = Field(alias="CLEAN_SESSION", default=None)
    retain: bool | None = Field(alias="RETAIN", default=None)
    qos: int | None = Field(alias="QOS", default=None)
    time_interval: int | None = Field(alias="TIME_INTERVAL", default=None)


class ClientSettings(BaseModel):
    clean_session: bool = Field(alias="CLEAN_SESSION")
    retain: bool = Field(alias="RETAIN")
    qos: int = Field(alias="QOS")
    time_interval: int = Field(alias="TIME_INTERVAL")

    @classmethod
    def from_partial(cls, partial: ClientSettingsPartial, default: ClientSettings) -> ClientSettings:
        def resolve[T](value: T | None, default_value: T) -> T:
            return value if value is not None else default_value

        return cls(
            CLEAN_SESSION=resolve(partial.clean_session, default.clean_session),
            RETAIN=resolve(partial.retain, default.retain),
            QOS=resolve(partial.qos, default.qos),
            TIME_INTERVAL=resolve(partial.time_interval, default.time_interval),
        )
