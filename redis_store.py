from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any

@dataclass
class ValueWithExpiry:
    value: Any
    expiresAt: datetime.time = 0


def is_expired(v: ValueWithExpiry) -> bool:
    if v.expiresAt == 0: return False

    return v.expiresAt < datetime.now()


class Storage:
    def __init__(self):
        self.map = dict()
    
    def set(self, key: str, value: str):
        self.map[key] = ValueWithExpiry(value)
    
    def set_with_expiry(self, key: str, value: str, expiry: timedelta):
        expires = datetime.now() + timedelta(milliseconds=expiry)
        self.map[key] = ValueWithExpiry(
            value=value,
            expiresAt=expires
        )
    
    def get(self, key):
        valueWithExpiry: ValueWithExpiry = self.map.get(key, None)
        
        if not valueWithExpiry:
            return "", False

        if is_expired(valueWithExpiry):
            del self.map[key]
            return "", False
        
        return valueWithExpiry.value, True