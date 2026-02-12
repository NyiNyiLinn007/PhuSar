from __future__ import annotations

from dataclasses import dataclass

import asyncpg

from app.db import Database


@dataclass(slots=True)
class UserRepository:
    db: Database

    async def ensure_user(self, user_id: int, full_name: str) -> asyncpg.Record:
        query = """
            INSERT INTO users (user_id, full_name)
            VALUES ($1, LEFT($2, 100))
            ON CONFLICT (user_id) DO UPDATE
            SET full_name = LEFT(EXCLUDED.full_name, 100),
                updated_at = CURRENT_TIMESTAMP
            RETURNING *;
        """
        return await self.db.fetchrow(query, user_id, full_name)  # type: ignore[return-value]

    async def get(self, user_id: int) -> asyncpg.Record | None:
        return await self.db.fetchrow("SELECT * FROM users WHERE user_id = $1;", user_id)

    async def get_language(self, user_id: int, default: str = "en") -> str:
        row = await self.db.fetchrow("SELECT language FROM users WHERE user_id = $1;", user_id)
        if not row:
            return default
        language = row["language"] or default
        return language if language in {"en", "my"} else default

    async def save_registration(
        self,
        user_id: int,
        language: str,
        gender: str,
        seeking: str,
        location_region: str,
        township: str,
        age: int,
        bio: str,
        photo_id: str,
    ) -> None:
        query = """
            UPDATE users
            SET language = $2,
                gender = $3,
                seeking = $4,
                location_region = LEFT($5, 50),
                township = LEFT($6, 50),
                age = $7,
                bio = LEFT($8, 500),
                photo_id = $9,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
        """
        await self.db.execute(
            query,
            user_id,
            language,
            gender,
            seeking,
            location_region,
            township,
            age,
            bio,
            photo_id,
        )

    async def set_language(self, user_id: int, language: str) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET language = $2, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            language,
        )

    async def set_premium(self, user_id: int, is_premium: bool) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET is_premium = $2, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            is_premium,
        )

    async def set_banned(self, user_id: int, is_banned: bool) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET is_banned = $2, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            is_banned,
        )

    async def list_candidate_ids(
        self,
        viewer_id: int,
        viewer_gender: str,
        seeking: str,
        limit: int = 80,
    ) -> list[int]:
        wanted_genders = ["male", "female"] if seeking == "both" else [seeking]
        query = """
            SELECT u.user_id
            FROM users u
            LEFT JOIN actions a
                ON a.actor_id = $1 AND a.target_id = u.user_id
            WHERE u.user_id != $1
              AND u.is_banned = FALSE
              AND u.gender = ANY($2::text[])
              AND (u.seeking = 'both' OR u.seeking = $3)
              AND u.photo_id IS NOT NULL
              AND u.age IS NOT NULL
              AND u.location_region IS NOT NULL
              AND u.township IS NOT NULL
              AND a.target_id IS NULL
            ORDER BY u.created_at DESC
            LIMIT $4;
        """
        rows = await self.db.fetch(query, viewer_id, wanted_genders, viewer_gender, limit)
        return [int(item["user_id"]) for item in rows]


@dataclass(slots=True)
class ActionRepository:
    db: Database

    async def save_action(self, actor_id: int, target_id: int, action_type: str) -> None:
        query = """
            INSERT INTO actions (actor_id, target_id, action_type)
            VALUES ($1, $2, $3)
            ON CONFLICT (actor_id, target_id) DO UPDATE
            SET action_type = EXCLUDED.action_type,
                created_at = CURRENT_TIMESTAMP;
        """
        await self.db.execute(query, actor_id, target_id, action_type)

    async def has_positive_action(self, actor_id: int, target_id: int) -> bool:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM actions
                WHERE actor_id = $1
                  AND target_id = $2
                  AND action_type IN ('like', 'superlike')
            ) AS matched;
        """
        row = await self.db.fetchrow(query, actor_id, target_id)
        return bool(row and row["matched"])


@dataclass(slots=True)
class PremiumRequestRepository:
    db: Database

    async def create(self, user_id: int, provider: str, screenshot_file_id: str) -> int:
        row = await self.db.fetchrow(
            """
            INSERT INTO premium_requests (user_id, provider, screenshot_file_id)
            VALUES ($1, $2, $3)
            RETURNING id;
            """,
            user_id,
            provider,
            screenshot_file_id,
        )
        if row is None:
            raise RuntimeError("Failed to create premium request.")
        return int(row["id"])

    async def get(self, request_id: int) -> asyncpg.Record | None:
        return await self.db.fetchrow("SELECT * FROM premium_requests WHERE id = $1;", request_id)

    async def set_status(self, request_id: int, status: str, reviewed_by: int) -> None:
        await self.db.execute(
            """
            UPDATE premium_requests
            SET status = $2,
                reviewed_by = $3,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = $1;
            """,
            request_id,
            status,
            reviewed_by,
        )


@dataclass(slots=True)
class ReportRepository:
    db: Database

    async def create(self, reporter_id: int, target_id: int, reason: str) -> int:
        row = await self.db.fetchrow(
            """
            INSERT INTO reports (reporter_id, target_id, reason)
            VALUES ($1, $2, $3)
            RETURNING id;
            """,
            reporter_id,
            target_id,
            reason,
        )
        if row is None:
            raise RuntimeError("Failed to create report.")
        return int(row["id"])

    async def get(self, report_id: int) -> asyncpg.Record | None:
        return await self.db.fetchrow("SELECT * FROM reports WHERE id = $1;", report_id)

    async def set_status(self, report_id: int, status: str, reviewed_by: int) -> None:
        await self.db.execute(
            """
            UPDATE reports
            SET status = $2,
                reviewed_by = $3,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = $1;
            """,
            report_id,
            status,
            reviewed_by,
        )
