from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetBySettingName(BaseEntity):
    setting_name: str