from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _parse_admin_ids(raw: str) -> set[int]:
    admin_ids: set[int] = set()
    for item in raw.split(","):
        value = item.strip()
        if not value:
            continue
        if value.isdigit():
            admin_ids.add(int(value))
    return admin_ids


@dataclass(slots=True)
class Settings:
    bot_token: str
    database_url: str
    redis_url: str
    admin_ids: set[int]
    default_language: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        database_url = os.getenv("DATABASE_URL", "").strip()
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0").strip()
        admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
        default_language = os.getenv("DEFAULT_LANGUAGE", "en").strip().lower()
        if default_language not in {"en", "my"}:
            default_language = "en"

        if not bot_token:
            raise ValueError("BOT_TOKEN is required.")
        if not database_url:
            raise ValueError("DATABASE_URL is required.")

        return cls(
            bot_token=bot_token,
            database_url=database_url,
            redis_url=redis_url,
            admin_ids=admin_ids,
            default_language=default_language,
        )
