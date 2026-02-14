from __future__ import annotations

from collections.abc import Awaitable, Callable
from time import monotonic
from typing import Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, min_interval_seconds: float = 1.0) -> None:
        self.min_interval_seconds = min_interval_seconds
        self._last_action_at: dict[int, float] = {}
        self._last_warn_at: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = self._extract_user_id(event, data)
        if user_id is None:
            return await handler(event, data)

        now = monotonic()
        last = self._last_action_at.get(user_id)
        if last is not None and now - last < self.min_interval_seconds:
            await self._warn_if_needed(event, user_id, now)
            return None

        self._last_action_at[user_id] = now
        return await handler(event, data)

    @staticmethod
    def _extract_user_id(event: TelegramObject, data: dict[str, Any]) -> int | None:
        if isinstance(event, Message) and event.from_user is not None:
            return event.from_user.id
        if isinstance(event, CallbackQuery) and event.from_user is not None:
            return event.from_user.id

        from_user = data.get("event_from_user")
        if from_user is not None and hasattr(from_user, "id"):
            try:
                return int(from_user.id)
            except (TypeError, ValueError):
                return None
        return None

    async def _warn_if_needed(self, event: TelegramObject, user_id: int, now: float) -> None:
        warn_interval = 3.0
        last_warn = self._last_warn_at.get(user_id, 0.0)
        if now - last_warn < warn_interval:
            return
        self._last_warn_at[user_id] = now

        try:
            if isinstance(event, CallbackQuery):
                await event.answer("Too many requests. Please wait a second.", show_alert=False)
            elif isinstance(event, Message):
                await event.answer("Too many requests. Please wait a second.")
        except TelegramAPIError:
            return
