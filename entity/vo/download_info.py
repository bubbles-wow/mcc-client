from dataclasses import dataclass

from . import BaseEntity

@dataclass
class DownloadInfo(BaseEntity):
    entity_id: str
    res_url: str