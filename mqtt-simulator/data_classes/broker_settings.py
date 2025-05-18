from typing import Optional
from dataclasses import dataclass

@dataclass
class BrokerSettings:
    url: str
    port: int
    protocol: int
    is_tls_enabled: bool = False
    tls_ca_path: Optional[str] = None
    tls_cert_path: Optional[str] = None
    tls_key_path: Optional[str] = None

    def __post_init__(self):
        self.is_tls_enabled = (
            self.tls_ca_path is not None or
            self.tls_cert_path is not None or
            self.tls_key_path is not None
        )
