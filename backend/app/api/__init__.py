"""API routes."""

from .chat import router as chat_router
from .documents import router as documents_router
from .health import router as health_router
from .weather import router as weather_router
from .maps import router as maps_router
from .traffic import router as traffic_router

__all__ = [
    "chat_router",
    "documents_router",
    "health_router",
    "weather_router",
    "maps_router",
    "traffic_router"
]
