from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot_commands import setup_default_commands
from app.config import Settings
from app.context import AppContext, set_app
from app.db import Database
from app.handlers import get_routers
from app.middlewares import ThrottlingMiddleware
from app.repositories import ActionRepository, PremiumRequestRepository, ReportRepository, UserRepository
from app.services import DiscoveryService


async def run() -> None:
    settings = Settings.from_env()
    db = Database(settings.database_url)
    await db.connect()
    await db.init_schema()

    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    storage = RedisStorage.from_url(settings.redis_url)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)
    throttle = ThrottlingMiddleware(min_interval_seconds=1.0)
    dp.message.outer_middleware(throttle)
    dp.callback_query.outer_middleware(throttle)

    users = UserRepository(db)
    actions = ActionRepository(db)
    premium_requests = PremiumRequestRepository(db)
    reports = ReportRepository(db)
    discovery = DiscoveryService(users, redis_client)

    context = AppContext(
        settings=settings,
        db=db,
        redis=redis_client,
        users=users,
        actions=actions,
        premium_requests=premium_requests,
        reports=reports,
        discovery=discovery,
    )
    set_app(context)

    for router in get_routers(settings.premium_enabled):
        dp.include_router(router)

    try:
        await setup_default_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()
        await redis_client.aclose()
        await db.close()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    asyncio.run(run())


if __name__ == "__main__":
    main()
