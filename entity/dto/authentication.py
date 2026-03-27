from dataclasses import dataclass
from typing import Optional, Any

from . import BaseEntity
from ..sauth import Sauth

@dataclass
class Authentication(BaseEntity):
    aid: Optional[int] = None
    otp_token: Optional[str] = None
    pay_channel: Optional[str] = "netease"
    sa_data: Optional[str] = None
    sauth_json: Optional[str] = None
    version: Optional[dict] = None