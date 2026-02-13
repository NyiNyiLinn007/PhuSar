from __future__ import annotations

from datetime import UTC, datetime
from collections.abc import Mapping
from html import escape
from math import acos, cos, radians, sin
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


def now_utc() -> datetime:
    return datetime.now(tz=UTC).replace(tzinfo=None)


def is_premium_active(user: Mapping[str, Any]) -> bool:
    premium_until = user.get("premium_until")
    if premium_until is None:
        return bool(user.get("is_premium"))
    if isinstance(premium_until, datetime):
        return premium_until > now_utc()
    return bool(user.get("is_premium"))


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    cosine_value = (
        cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon2) - radians(lon1))
        + sin(radians(lat1)) * sin(radians(lat2))
    )
    clamped = max(-1.0, min(1.0, cosine_value))
    return 6371.0 * acos(clamped)


def distance_between_users_km(viewer: Mapping[str, Any], candidate: Mapping[str, Any]) -> float | None:
    viewer_lat = viewer.get("latitude")
    viewer_lon = viewer.get("longitude")
    candidate_lat = candidate.get("latitude")
    candidate_lon = candidate.get("longitude")

    if viewer_lat is None or viewer_lon is None or candidate_lat is None or candidate_lon is None:
        return None
    try:
        return haversine_km(float(viewer_lat), float(viewer_lon), float(candidate_lat), float(candidate_lon))
    except (TypeError, ValueError):
        return None
