from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from redis.asyncio import Redis

from app.config import Settings
from app.context import AppContext, set_app
from app.db import Database
from app.handlers import get_routers
from app.middlewares import ThrottlingMiddleware
from app.repositories import ActionRepository, PremiumRequestRepository, ReportRepository, UserRepository
from app.services import DiscoveryService


@dataclass(slots=True)
class RuntimeResources:
    settings: Settings
    db: Database
    redis: Redis
    bot: Bot
    dp: Dispatcher


async def _build_runtime(settings: Settings) -> RuntimeResources:
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

    return RuntimeResources(
        settings=settings,
        db=db,
        redis=redis_client,
        bot=bot,
        dp=dp,
    )


async def _healthcheck(_: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


async def _on_startup(app: web.Application) -> None:
    runtime: RuntimeResources = app["runtime"]
    await runtime.bot.set_webhook(
        url=runtime.settings.webhook_url,
        secret_token=runtime.settings.webhook_secret_token,
        allowed_updates=runtime.dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info("Webhook set to %s", runtime.settings.webhook_url)


async def _on_shutdown(app: web.Application) -> None:
    runtime: RuntimeResources = app["runtime"]
    await runtime.dp.storage.close()
    await runtime.bot.session.close()
    await runtime.redis.aclose()
    await runtime.db.close()


async def _create_web_app() -> web.Application:
    settings = Settings.from_env()
    if not settings.webhook_url:
        raise ValueError("WEBHOOK_URL is required in webhook mode.")
    if not settings.webhook_secret_token:
        raise ValueError("WEBHOOK_SECRET_TOKEN is required in webhook mode.")

    runtime = await _build_runtime(settings)
    @web.middleware
    async def webhook_secret_middleware(
        request: web.Request,
        handler,
    ) -> web.StreamResponse:
        if request.method == "POST" and request.path == settings.webhook_path:
            provided = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if provided != settings.webhook_secret_token:
                return web.Response(status=401, text="Unauthorized")
        return await handler(request)

    web_app = web.Application(middlewares=[webhook_secret_middleware])
    web_app["runtime"] = runtime

    SimpleRequestHandler(
        dispatcher=runtime.dp,
        bot=runtime.bot,
        secret_token=settings.webhook_secret_token,
    ).register(web_app, path=settings.webhook_path)

    setup_application(web_app, runtime.dp, bot=runtime.bot)
    web_app.router.add_get("/", _healthcheck)
    web_app.router.add_get("/healthz", _healthcheck)
    web_app.on_startup.append(_on_startup)
    web_app.on_shutdown.append(_on_shutdown)
    return web_app


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    web_app = asyncio.run(_create_web_app())
    runtime: RuntimeResources = web_app["runtime"]
    web.run_app(web_app, host="0.0.0.0", port=runtime.settings.port)


if __name__ == "__main__":
    main()
