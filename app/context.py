from __future__ import annotations

from dataclasses import dataclass

from aiogram import Bot
from redis.asyncio import Redis

from app.config import Settings
from app.db import Database
from app.repositories import ActionRepository, PremiumRequestRepository, ReportRepository, UserRepository
from app.services import DiscoveryService


@dataclass(slots=True)
class AppContext:
    settings: Settings
    db: Database
    redis: Redis
    users: UserRepository
    actions: ActionRepository
    premium_requests: PremiumRequestRepository
    reports: ReportRepository
    discovery: DiscoveryService


_APP_CONTEXT: AppContext | None = None


def set_app(app: AppContext) -> None:
    global _APP_CONTEXT
    _APP_CONTEXT = app


def get_app(bot: Bot | None = None) -> AppContext:
    del bot
    if _APP_CONTEXT is None:
        raise RuntimeError("Application context is not initialized.")
    return _APP_CONTEXT
