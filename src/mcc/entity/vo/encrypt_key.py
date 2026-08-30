from dataclasses import dataclass

from . import BaseEntity

@dataclass
class EncryptKey(BaseEntity):
    item_id: str
    jwt: str