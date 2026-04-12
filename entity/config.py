from dataclasses import dataclass, field
from typing import Any, Optional

from . import BaseEntity
from .sa_data import SaData
from .sauth import Sauth

@dataclass
class SessionConfig(BaseEntity):
    path: str = "session/"
    expired: int = 1800
    timezone: int = 0
    file_name: str = "{server_type}_{server_env}.session"
    
@dataclass
class ApiDetailConfig(BaseEntity):
    host: str = ""
    path: str = ""
    encrypt_body_type: int = 0
    extra_param: Optional[dict] = field(default_factory=dict)

@dataclass
class ApiConfig(BaseEntity):
    login_otp: ApiDetailConfig = field(default_factory=ApiDetailConfig)
    authentication_otp: ApiDetailConfig = field(default_factory=ApiDetailConfig)
    authentication_update: ApiDetailConfig = field(default_factory=ApiDetailConfig)
    pe_authentication: ApiDetailConfig = field(default_factory=ApiDetailConfig)

@dataclass
class ServerDetailConfig(BaseEntity):
    serverlist_url: str
    api_config: ApiConfig = field(default_factory=ApiConfig)
    api_host_flag: int = 1
    
@dataclass
class PeClientConfig(BaseEntity):
    engine_version: str
    engine_hash: str
    patch_version: str
    patch_hash: str
    sign_hash: str = "2b3e7ca013bb30a74d822579860c042b"
    sign_sp: int = 3
    sign_tr: int = 9
    pay_channel: str = "netease"

@dataclass
class PcClientConfig(BaseEntity):
    version: str = "1.15.18.46492"
    
@dataclass
class ClientConfig(BaseEntity):
    type: str = "pc"
    config: Optional[PeClientConfig | PcClientConfig] = field(default_factory=PcClientConfig)
    sa_data: Optional[SaData] = None

    @classmethod
    def from_any(cls, data: Any) -> "ClientConfig":
        if data is None:
            return cls()
        
        if not isinstance(data, dict):
            return super().from_any(data)

        client_type = data.get("type", "pc")
        processed_data = data.copy()
        raw_config = data.get("config")

        if raw_config:
            if client_type == "pe":
                processed_data["config"] = PeClientConfig.from_any(raw_config)
            else:
                processed_data["config"] = PcClientConfig.from_any(raw_config)
        
        return super().from_any(processed_data)
    
@dataclass
class AccountConfig(BaseEntity):
    sa_data: SaData = field(default_factory=SaData)
    sauth: Sauth = field(default_factory=Sauth)

@dataclass
class X19Config(BaseEntity):
    session: SessionConfig = field(default_factory=SessionConfig)
    client: dict[str, ClientConfig] = field(default_factory=dict)
    account: dict[str, Sauth] = field(default_factory=dict)
    server: dict[str, dict[str, ServerDetailConfig]] = field(default_factory=dict)
