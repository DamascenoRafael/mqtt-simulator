from dataclasses import dataclass

@dataclass
class BrokerSettings:
    url: str
    port: int
    protocol: int
