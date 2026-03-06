from dataclasses import dataclass

from . import BaseEntity

@dataclass
class Serverlist(BaseEntity):
    core_server_url: str
    web_server_url: str
    dc_web_url: str
    api_gateway_url: str