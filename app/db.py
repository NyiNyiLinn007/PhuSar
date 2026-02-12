from __future__ import annotations

from pathlib import Path

import asyncpg


class Database:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=10)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def execute(self, query: str, *args: object) -> str:
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args: object) -> list[asyncpg.Record]:
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args: object) -> asyncpg.Record | None:
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def init_schema(self) -> None:
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        schema_path = Path(__file__).resolve().parent.parent / "db" / "init.sql"
        sql = schema_path.read_text(encoding="utf-8")
        statements = [item.strip() for item in sql.split(";") if item.strip()]
        async with self.pool.acquire() as conn:
            for statement in statements:
                await conn.execute(statement)
