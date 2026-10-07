import uuid

from dataclasses import dataclass, fields

from typing import Optional, Any
from . import BaseEntity

@dataclass
class Sauth(BaseEntity):
    access_token: Optional[str] = None
    aim_info: str = r'{"aim":"127.0.0.1","country":"CN","tz":"+0800","tzid":"Asia\/Hong_Kong","celluar_ip":"","operator":"460000","is_vpn_enabled":false}'
    app_channel: str = "a50_sdk_cn"
    client_login_sn: str = uuid.uuid4().hex.upper()
    deviceid: Optional[str] = None
    gameid: str = "x19"
    gas_token: str = ""
    get_access_token: str = "0"
    ip: str = "127.0.0.1"
    login_channel: str = "netease"
    platform: str = "pc"
    sdk_version: str = "4.16.0"
    sdkuid: Optional[str] = None
    sessionid: Optional[str] = None
    source_app_channel: str = "a50_sdk_cn"
    source_platform: str = "pc"
    step: Optional[str] = None
    step2: Optional[str] = None
    tdid: Optional[str] = None
    udid: Optional[str] = None
