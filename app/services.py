from __future__ import annotations

import asyncpg
from redis.asyncio import Redis

from app.repositories import UserRepository


class DiscoveryService:
    def __init__(self, users: UserRepository, redis_client: Redis) -> None:
        self.users = users
        self.redis = redis_client

    @staticmethod
    def _queue_key(user_id: int) -> str:
        return f"discover_queue:{user_id}"

    async def clear_queue(self, user_id: int) -> None:
        await self.redis.delete(self._queue_key(user_id))

    async def next_candidate_id(self, viewer: asyncpg.Record) -> int | None:
        viewer_id = int(viewer["user_id"])
        queue_key = self._queue_key(viewer_id)
        candidate_raw = await self.redis.lpop(queue_key)

        if candidate_raw is None:
            candidate_ids = await self.users.list_candidate_ids(
                viewer_id=viewer_id,
                viewer_gender=viewer["gender"],
                seeking=viewer["seeking"],
            )
            if not candidate_ids:
                return None
            await self.redis.rpush(queue_key, *[str(user_id) for user_id in candidate_ids])
            candidate_raw = await self.redis.lpop(queue_key)

        if candidate_raw is None:
            return None
        return int(candidate_raw)
