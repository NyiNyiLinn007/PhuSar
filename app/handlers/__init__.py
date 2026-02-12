from app.handlers.admin import router as admin_router
from app.handlers.discovery import router as discovery_router
from app.handlers.premium import router as premium_router
from app.handlers.registration import router as registration_router
from app.handlers.start import router as start_router

ROUTERS = [
    registration_router,
    start_router,
    discovery_router,
    premium_router,
    admin_router,
]
