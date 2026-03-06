from dataclasses import dataclass, field

from . import BaseEntity

@dataclass
class GetEncryptKeyList(BaseEntity):
    """
    /pe-item/get-encryption-key-list
    
    Attributes:
        device_id: str, default "123456"
        item_ids: list[str], list of item_id to get encrypt key
    """
    device_id: str = "123456"
    item_ids: list[str] = field(default_factory=list)