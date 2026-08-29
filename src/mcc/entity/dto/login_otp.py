from dataclasses import dataclass

from . import BaseEntity

@dataclass
class LoginOtp(BaseEntity):
    sauth_json: str