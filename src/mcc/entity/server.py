from dataclasses import dataclass

from . import BaseEntity
from .serverlist import Serverlist

@dataclass
class Server(BaseEntity):
    serverlist_url: str
    server_env: str
    server_code: str
    api_host_flag: int
    etag: str
    last_modified: str
    serverlist: Serverlist
    