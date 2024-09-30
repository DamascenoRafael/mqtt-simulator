from dataclasses import dataclass

@dataclass
class ClientSettings:
    clean: bool
    retain: bool
    qos: int
    time_interval: int
