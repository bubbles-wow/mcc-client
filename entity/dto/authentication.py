from dataclasses import dataclass
from typing import Optional, Any

from . import BaseEntity
from ..sauth import Sauth

@dataclass
class Authentication(BaseEntity):
    aid: Optional[int] = None
    engine_version: Optional[str] = None
    extra_param: Optional[str] = "extra"
    message: Optional[str] = None
    otp_token: Optional[str] = None
    patch_version: Optional[str] = None
    pay_channel: Optional[str] = "netease"
    sa_data: Optional[str] = None
    sauth_json: Optional[str|Sauth] = None
    seed: Optional[str] = None
    sign: Optional[str] = None
    version: Optional[dict] = None