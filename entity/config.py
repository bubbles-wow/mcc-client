from dataclasses import dataclass, field
from typing import Optional

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
    pay_channel: str = "netease"

@dataclass
class PcClientConfig(BaseEntity):
    version: str = "1.15.18.46492"
    
@dataclass
class ClientConfig(BaseEntity):
    android: PeClientConfig = field(default_factory=PeClientConfig)
    pc_cocos: PeClientConfig = field(default_factory=PeClientConfig)
    pc: PcClientConfig = field(default_factory=PcClientConfig)

@dataclass
class X19Config(BaseEntity):
    session: SessionConfig = field(default_factory=SessionConfig)
    client: ClientConfig = field(default_factory=ClientConfig)
    sa_data: SaData = field(default_factory=SaData)
    sauth: Sauth = field(default_factory=Sauth)
    server: dict[str, dict[str, ServerDetailConfig]] = field(default_factory=dict)
