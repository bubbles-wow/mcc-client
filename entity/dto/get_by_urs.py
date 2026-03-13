from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetByUrs(BaseEntity):
    urs: str