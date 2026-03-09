from dataclasses import dataclass

from . import BaseEntity

@dataclass
class Otp(BaseEntity):
    otp: int
    otp_token: str
    aid: int
    lock_time: int
    open_otp: int