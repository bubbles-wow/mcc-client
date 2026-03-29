import re
import random

from typing import Any
from importlib.util import find_spec
if find_spec("common.util.string") is not None:
    from common.util.string import *
else:
    from string import *

def to_snake_case(name: str) -> str:
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    s2 = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return s2.lower()

def convert_keys_to_snake(data: Any) -> Any:
    if isinstance(data, dict):
        return {to_snake_case(k): convert_keys_to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake(i) for i in data]
    return data

def rand_string_runes(n: int) -> str:
    letters = ascii_letters + digits
    return ''.join(random.choice(letters) for _ in range(n))

def is_empty(s: str) -> bool:
    return s is None or s.strip() == ""

def save_format(original: str, template: dict[str, str]) -> str:
    for key, val in template.items():
        original = original.replace(f"{{{key}}}", str(val))
    return original