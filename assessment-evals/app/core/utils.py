from typing import Any
import json

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


def load_error_json(error_message) -> str:
    details = json.loads(error_message.text)
    error_details = details.get("detail")
    return error_details

