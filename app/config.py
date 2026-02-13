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


def _parse_bool(raw: str, default: bool) -> bool:
    value = raw.strip().lower()
    if not value:
        return default
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_int(raw: str, default: int) -> int:
    value = raw.strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(slots=True)
class Settings:
    bot_token: str
    database_url: str
    redis_url: str
    webhook_url: str
    webhook_path: str
    webhook_secret_token: str
    port: int
    admin_ids: set[int]
    premium_enabled: bool
    payment_phone: str
    kbzpay_qr_file_id: str
    wavemoney_qr_file_id: str
    default_language: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        database_url = os.getenv("DATABASE_URL", "").strip()
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0").strip()
        webhook_url = os.getenv("WEBHOOK_URL", "").strip()
        webhook_path = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
        if not webhook_path.startswith("/"):
            webhook_path = f"/{webhook_path}"
        webhook_secret_token = os.getenv("WEBHOOK_SECRET_TOKEN", "").strip()
        port = _parse_int(os.getenv("PORT", "8000"), 8000)
        admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
        premium_enabled = _parse_bool(os.getenv("PREMIUM_ENABLED", "false"), False)
        payment_phone = os.getenv("PAYMENT_PHONE", "").strip()
        kbzpay_qr_file_id = os.getenv("KBZPAY_QR_FILE_ID", "").strip()
        wavemoney_qr_file_id = os.getenv("WAVEMONEY_QR_FILE_ID", "").strip()
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
            webhook_url=webhook_url,
            webhook_path=webhook_path,
            webhook_secret_token=webhook_secret_token,
            port=port,
            admin_ids=admin_ids,
            premium_enabled=premium_enabled,
            payment_phone=payment_phone,
            kbzpay_qr_file_id=kbzpay_qr_file_id,
            wavemoney_qr_file_id=wavemoney_qr_file_id,
            default_language=default_language,
        )
