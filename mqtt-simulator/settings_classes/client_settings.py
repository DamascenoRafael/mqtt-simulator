from __future__ import annotations

from pydantic import BaseModel, Field


class ClientSettings(BaseModel):
    clean_session: bool | None = Field(alias="CLEAN_SESSION", default=None)
    retain: bool | None = Field(alias="RETAIN", default=None)
    qos: int | None = Field(alias="QOS", default=None)
    time_interval: int | None = Field(alias="TIME_INTERVAL", default=None)

    def resolve_with_default(self, default: ClientSettings) -> ClientSettings:
        def resolve[T](value: T, default_value: T) -> T:
            return value if value is not None else default_value

        return ClientSettings(
            CLEAN_SESSION=resolve(self.clean_session, default.clean_session),
            RETAIN=resolve(self.retain, default.retain),
            QOS=resolve(self.qos, default.qos),
            TIME_INTERVAL=resolve(self.time_interval, default.time_interval),
        )
