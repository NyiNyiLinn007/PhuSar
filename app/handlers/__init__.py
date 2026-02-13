from __future__ import annotations

from aiogram import Router

from app.handlers.admin import router as admin_router
from app.handlers.discovery import router as discovery_router
from app.handlers.premium import router as premium_router
from app.handlers.registration import router as registration_router
from app.handlers.start import router as start_router


def get_routers(premium_enabled: bool) -> list[Router]:
    routers: list[Router] = [
        registration_router,
        start_router,
        discovery_router,
        admin_router,
    ]
    if premium_enabled:
        routers.append(premium_router)
    return routers
