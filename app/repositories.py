from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import asyncpg

from app.db import Database
from app.utils import now_utc


@dataclass(slots=True)
class UserRepository:
    db: Database

    async def ensure_user(self, user_id: int, full_name: str) -> asyncpg.Record:
        query = """
            INSERT INTO users (user_id, full_name)
            VALUES ($1, LEFT($2, 100))
            ON CONFLICT (user_id) DO UPDATE
            SET full_name = COALESCE(NULLIF(users.full_name, ''), LEFT(EXCLUDED.full_name, 100)),
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
        full_name: str,
        language: str,
        gender: str,
        seeking: str,
        location_region: str,
        township: str,
        age: int,
        bio: str,
        photo_id: str,
        latitude: float | None,
        longitude: float | None,
    ) -> None:
        query = """
            UPDATE users
            SET full_name = LEFT($2, 100),
                language = $3,
                gender = $4,
                seeking = $5,
                location_region = LEFT($6, 50),
                township = LEFT($7, 50),
                age = $8,
                bio = LEFT($9, 500),
                photo_id = $10,
                latitude = $11,
                longitude = $12,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
        """
        await self.db.execute(
            query,
            user_id,
            full_name,
            language,
            gender,
            seeking,
            location_region,
            township,
            age,
            bio,
            photo_id,
            latitude,
            longitude,
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

    async def update_coordinates(self, user_id: int, latitude: float, longitude: float) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET latitude = $2,
                longitude = $3,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            latitude,
            longitude,
        )

    async def set_premium_until(self, user_id: int, premium_until: datetime | None) -> None:
        is_premium = premium_until is not None and premium_until > now_utc()
        await self.db.execute(
            """
            UPDATE users
            SET is_premium = $2,
                premium_until = $3,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            is_premium,
            premium_until,
        )

    async def refresh_like_window(self, user_id: int) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET likes_today = CASE
                WHEN likes_reset_at IS NULL OR likes_reset_at < CURRENT_TIMESTAMP - INTERVAL '24 hours'
                    THEN 0
                ELSE likes_today
            END,
                likes_reset_at = CASE
                    WHEN likes_reset_at IS NULL OR likes_reset_at < CURRENT_TIMESTAMP - INTERVAL '24 hours'
                        THEN CURRENT_TIMESTAMP
                    ELSE likes_reset_at
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
        )

    async def set_like_cache(self, user_id: int, likes_today: int) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET likes_today = $2, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1;
            """,
            user_id,
            likes_today,
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
        viewer_latitude: float | None,
        viewer_longitude: float | None,
        viewer_region: str | None,
        limit: int = 80,
    ) -> list[int]:
        wanted_genders = ["male", "female"] if seeking == "both" else [seeking]
        query = """
            WITH pool AS (
                SELECT
                    u.user_id,
                    u.location_region,
                    u.created_at,
                    CASE
                        WHEN $4::double precision IS NULL
                             OR $5::double precision IS NULL
                             OR u.latitude IS NULL
                             OR u.longitude IS NULL
                            THEN NULL
                        ELSE 6371 * acos(
                            LEAST(1.0, GREATEST(-1.0,
                                cos(radians($4::double precision)) * cos(radians(u.latitude))
                                * cos(radians(u.longitude) - radians($5::double precision))
                                + sin(radians($4::double precision)) * sin(radians(u.latitude))
                            ))
                        )
                    END AS distance_km
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
            )
            SELECT user_id
            FROM pool
            ORDER BY
                CASE
                    WHEN distance_km IS NOT NULL AND distance_km < 50 THEN 0
                    WHEN distance_km IS NOT NULL THEN 1
                    ELSE 2
                END,
                distance_km NULLS LAST,
                (location_region = COALESCE($6, location_region)) DESC,
                created_at DESC
            LIMIT $7;
        """
        rows = await self.db.fetch(
            query,
            viewer_id,
            wanted_genders,
            viewer_gender,
            viewer_latitude,
            viewer_longitude,
            viewer_region,
            limit,
        )
        return [int(item["user_id"]) for item in rows]

    async def list_boost_viewer_ids(
        self,
        actor_id: int,
        actor_gender: str,
        actor_seeking: str,
        actor_region: str | None,
        limit: int = 100,
    ) -> list[int]:
        viewer_genders = ["male", "female"] if actor_seeking == "both" else [actor_seeking]
        query = """
            SELECT u.user_id
            FROM users u
            LEFT JOIN actions a
                ON a.actor_id = u.user_id AND a.target_id = $1
            WHERE u.user_id != $1
              AND u.is_banned = FALSE
              AND u.gender = ANY($2::text[])
              AND (u.seeking = 'both' OR u.seeking = $3)
              AND u.photo_id IS NOT NULL
              AND u.age IS NOT NULL
              AND a.target_id IS NULL
              AND ($4::text IS NULL OR u.location_region = $4)
            ORDER BY u.created_at DESC
            LIMIT $5;
        """
        rows = await self.db.fetch(query, actor_id, viewer_genders, actor_gender, actor_region, limit)
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

    async def delete_action(self, actor_id: int, target_id: int) -> None:
        await self.db.execute(
            """
            DELETE FROM actions
            WHERE actor_id = $1 AND target_id = $2;
            """,
            actor_id,
            target_id,
        )

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

    async def count_recent_positive(self, actor_id: int, hours: int = 24) -> int:
        row = await self.db.fetchrow(
            """
            SELECT COUNT(*)::int AS total
            FROM actions
            WHERE actor_id = $1
              AND action_type IN ('like', 'superlike')
              AND created_at >= CURRENT_TIMESTAMP - ($2::text || ' hours')::interval;
            """,
            actor_id,
            hours,
        )
        if row is None:
            return 0
        return int(row["total"])

    async def list_incoming_likes(self, target_id: int, limit: int = 50) -> list[asyncpg.Record]:
        query = """
            SELECT u.*, a.created_at AS liked_at, a.action_type
            FROM actions a
            JOIN users u ON u.user_id = a.actor_id
            LEFT JOIN actions mine
                ON mine.actor_id = $1 AND mine.target_id = a.actor_id
            WHERE a.target_id = $1
              AND a.action_type IN ('like', 'superlike')
              AND u.is_banned = FALSE
              AND mine.actor_id IS NULL
            ORDER BY a.created_at DESC
            LIMIT $2;
        """
        return await self.db.fetch(query, target_id, limit)


@dataclass(slots=True)
class PremiumRequestRepository:
    db: Database

    async def create(
        self,
        user_id: int,
        provider: str,
        plan_code: str,
        duration_days: int,
        price_mmk: int,
        screenshot_file_id: str,
    ) -> int:
        row = await self.db.fetchrow(
            """
            INSERT INTO premium_requests (user_id, provider, plan_code, duration_days, price_mmk, screenshot_file_id)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
            """,
            user_id,
            provider,
            plan_code,
            duration_days,
            price_mmk,
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

    async def resolve_latest_pending_for_user(
        self,
        user_id: int,
        status: str,
        reviewed_by: int,
    ) -> asyncpg.Record | None:
        return await self.db.fetchrow(
            """
            WITH pending AS (
                SELECT id
                FROM premium_requests
                WHERE user_id = $1 AND status = 'pending'
                ORDER BY created_at DESC
                LIMIT 1
            )
            UPDATE premium_requests p
            SET status = $2,
                reviewed_by = $3,
                reviewed_at = CURRENT_TIMESTAMP
            FROM pending
            WHERE p.id = pending.id
            RETURNING p.*;
            """,
            user_id,
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
