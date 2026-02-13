from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Database:
    def __init__(self, dsn: str) -> None:
        self.dsn, self.connect_args = self._normalize_dsn(dsn)
        self.engine: AsyncEngine | None = None
        self._arg_pattern = re.compile(r"\$(\d+)")
        self._cast_bind_pattern = re.compile(
            r":p(\d+)::([a-zA-Z_][a-zA-Z0-9_]*(?:\[\])?(?:\s+[a-zA-Z_][a-zA-Z0-9_]*)*)"
        )

    @staticmethod
    def _normalize_dsn(dsn: str) -> tuple[str, dict[str, object]]:
        value = dsn.strip()
        if value.startswith("postgres://"):
            value = f"postgresql://{value[len('postgres://'):]}"
        if value.startswith("postgresql://"):
            value = f"postgresql+asyncpg://{value[len('postgresql://'):]}"

        parsed = urlsplit(value)
        query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
        cleaned_pairs: list[tuple[str, str]] = []
        connect_args: dict[str, object] = {}
        unsupported_params = {
            "channel_binding",
            "gssencmode",
        }
        has_ssl_param = any(key.lower() == "ssl" for key, _ in query_pairs)
        for key, val in query_pairs:
            if key.lower() in unsupported_params:
                # These libpq parameters are not accepted by asyncpg.
                continue
            if key.lower() == "sslmode":
                # asyncpg uses "ssl", not "sslmode"
                if val and not has_ssl_param:
                    sslmode = val.strip().lower()
                    if sslmode == "disable":
                        connect_args["ssl"] = False
                    else:
                        connect_args["ssl"] = True
                continue
            cleaned_pairs.append((key, val))

        normalized = urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                urlencode(cleaned_pairs, doseq=True),
                parsed.fragment,
            )
        )
        return normalized, connect_args

    def _compile_query(self, query: str, args: tuple[object, ...]) -> tuple[str, dict[str, object]]:
        sql = self._arg_pattern.sub(lambda match: f":p{match.group(1)}", query)
        # SQLAlchemy text() cannot always parse bind params followed by ::type.
        # Rewrite to CAST(:pN AS type) so asyncpg gets valid compiled SQL.
        sql = self._cast_bind_pattern.sub(
            lambda match: f"CAST(:p{match.group(1)} AS {match.group(2)})",
            sql,
        )
        params = {f"p{index}": value for index, value in enumerate(args, start=1)}
        return sql, params

    async def connect(self) -> None:
        self.engine = create_async_engine(
            self.dsn,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=10,
            connect_args=self.connect_args,
        )

    async def close(self) -> None:
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None

    async def execute(self, query: str, *args: object) -> str:
        if self.engine is None:
            raise RuntimeError("Database engine is not initialized.")
        sql, params = self._compile_query(query, args)
        async with self.engine.begin() as conn:
            result = await conn.execute(text(sql), params)
        affected = result.rowcount if result.rowcount is not None else 0
        return f"OK {affected}"

    async def fetch(self, query: str, *args: object) -> list[RowMapping]:
        if self.engine is None:
            raise RuntimeError("Database engine is not initialized.")
        sql, params = self._compile_query(query, args)
        async with self.engine.begin() as conn:
            result = await conn.execute(text(sql), params)
            rows = result.mappings().all()
        return list(rows)

    async def fetchrow(self, query: str, *args: object) -> RowMapping | None:
        if self.engine is None:
            raise RuntimeError("Database engine is not initialized.")
        sql, params = self._compile_query(query, args)
        async with self.engine.begin() as conn:
            result = await conn.execute(text(sql), params)
            row = result.mappings().first()
        return row

    async def init_schema(self) -> None:
        if self.engine is None:
            raise RuntimeError("Database engine is not initialized.")
        schema_path = Path(__file__).resolve().parent.parent / "db" / "init.sql"
        sql = schema_path.read_text(encoding="utf-8")
        statements = [item.strip() for item in sql.split(";") if item.strip()]
        async with self.engine.begin() as conn:
            for statement in statements:
                await conn.execute(text(statement))
