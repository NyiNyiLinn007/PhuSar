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

    @staticmethod
    def _rewind_key(user_id: int) -> str:
        return f"rewind_last_dislike:{user_id}"

    async def clear_queue(self, user_id: int) -> None:
        await self.redis.delete(self._queue_key(user_id))

    async def push_candidates(self, viewer_id: int, candidate_ids: list[int], to_front: bool = False) -> None:
        if not candidate_ids:
            return
        queue_key = self._queue_key(viewer_id)
        if to_front:
            await self.redis.lpush(queue_key, *[str(item) for item in candidate_ids[::-1]])
            return
        await self.redis.rpush(queue_key, *[str(item) for item in candidate_ids])

    async def push_candidate_to_viewers(self, candidate_id: int, viewer_ids: list[int]) -> None:
        if not viewer_ids:
            return
        async with self.redis.pipeline(transaction=False) as pipe:
            for viewer_id in viewer_ids:
                pipe.lpush(self._queue_key(viewer_id), str(candidate_id))
            await pipe.execute()

    async def set_last_disliked(self, user_id: int, target_id: int) -> None:
        await self.redis.set(self._rewind_key(user_id), str(target_id), ex=24 * 60 * 60)

    async def pop_last_disliked(self, user_id: int) -> int | None:
        key = self._rewind_key(user_id)
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.get(key)
            pipe.delete(key)
            value, _ = await pipe.execute()
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    async def next_candidate_id(self, viewer: asyncpg.Record) -> int | None:
        viewer_id = int(viewer["user_id"])
        queue_key = self._queue_key(viewer_id)
        candidate_raw = await self.redis.lpop(queue_key)

        if candidate_raw is None:
            candidate_ids = await self.users.list_candidate_ids(
                viewer_id=viewer_id,
                viewer_gender=viewer["gender"],
                seeking=viewer["seeking"],
                viewer_latitude=viewer["latitude"],
                viewer_longitude=viewer["longitude"],
                viewer_region=viewer["location_region"],
            )
            if not candidate_ids:
                return None
            await self.redis.rpush(queue_key, *[str(user_id) for user_id in candidate_ids])
            candidate_raw = await self.redis.lpop(queue_key)

        if candidate_raw is None:
            return None
        return int(candidate_raw)
