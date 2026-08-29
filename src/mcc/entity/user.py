from dataclasses import dataclass
from typing import Any

from . import BaseEntity

@dataclass
class User(BaseEntity):
    entity_id: str
    account: str
    token: str
    sead: str
    has_message: bool
    aid: int
    sdkuid: str
    access_token: str
    unisdk_login_json: str
    verify_status: int
    has_gmail: bool
    is_register: bool
    autopatch: list[Any]
    env: str
    last_server_up_time: int
    min_engine_version: str
    min_patch_version: str
