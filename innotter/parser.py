from typing import Optional


def parse_bool(value: Optional[str], default: bool = False) -> bool:
    if isinstance(value, str):
        if value.lower() in ["true", "1"]:
            return True
        elif value.lower() in ["false", "0"]:
            return False
    return default
