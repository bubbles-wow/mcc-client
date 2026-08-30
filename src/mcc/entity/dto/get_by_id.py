from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetById(BaseEntity):
    id: str