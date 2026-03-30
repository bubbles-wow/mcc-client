from dataclasses import dataclass, fields
from typing import Optional, Any

from . import BaseEntity
from ..sauth import Sauth
from ..sa_data import SaData

@dataclass
class PeAuthentication(BaseEntity):
    engine_version: Optional[str] = None
    extra_param: Optional[str] = "extra"
    message: Optional[str] = None
    patch_version: Optional[str] = None
    pay_channel: Optional[str] = "netease"
    sa_data: Optional[str] = None
    sauth_json: Optional[Sauth] = None
    seed: Optional[str] = None
    sign: Optional[str] = None
    version: Optional[dict] = None
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        if isinstance(self.sa_data, SaData) and self.sa_data.os_name == "windows":
            del result["sauth_json"]["step"]
            del result["sauth_json"]["step2"]
        return result