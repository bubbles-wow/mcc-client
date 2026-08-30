from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SettingValue(BaseEntity):
    setting_value: str