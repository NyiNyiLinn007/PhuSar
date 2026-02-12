from __future__ import annotations

from collections.abc import Mapping
from html import escape
from typing import Any


def is_profile_complete(user: Mapping[str, Any]) -> bool:
    required_fields = [
        "language",
        "gender",
        "seeking",
        "location_region",
        "township",
        "age",
        "bio",
        "photo_id",
    ]
    for field in required_fields:
        value = user.get(field)
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
    return True


def text(value: object) -> str:
    return escape(str(value) if value is not None else "")
