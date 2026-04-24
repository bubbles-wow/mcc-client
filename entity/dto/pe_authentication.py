import json

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
        sa_data_obj = SaData.from_any(json.loads(self.sa_data))
        if isinstance(sa_data_obj, SaData) and sa_data_obj.os_name == "windows":
            del result["sauth_json"]["step"]
            del result["sauth_json"]["step2"]
        else:
            result["sauth_json"]["sdk_version"] = sa_data_obj.sdk_ver
            result["sauth_json"]["platform"] = "ad"
            result["sauth_json"]["source_platform"] = "ad"
        del sa_data_obj
        return result