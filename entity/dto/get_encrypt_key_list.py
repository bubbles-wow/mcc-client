from dataclasses import dataclass, field

from . import BaseEntity

@dataclass
class GetEncryptKeyList(BaseEntity):
    item_ids: list[str]
    device_id: str = "123456"