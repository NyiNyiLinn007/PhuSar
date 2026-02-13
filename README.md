# Phu Sar Telegram Dating Bot

Production-ready starter for a Myanmar-focused Telegram dating bot built with `aiogram 3.x`, PostgreSQL, and Redis.

## Features

- FSM registration flow:
  - Language selection (English / Unicode Burmese)
  - Display name
  - Gender + seeking preferences
  - Region + township
  - Age, bio, photo upload validation
- Discovery engine:
  - Candidate filtering by seeking preference + region priority
  - Actions: `Like`, `Pass`
  - Mutual-like match notifications
  - Unlimited likes for all users
- Moderation:
  - In-app report button on each profile
  - Admin review and one-click ban workflow
- Deployment:
  - Docker + `docker-compose` with PostgreSQL and Redis

## Premium Module (Disabled by Default)

Premium code is kept in the project but hidden by default.

- Set `PREMIUM_ENABLED=false` to keep premium fully off.
- Set `PREMIUM_ENABLED=true` to re-enable premium menus and flows.

## Project Structure

```text
app/
  handlers/
  config.py
  db.py
  repositories.py
  services.py
  main.py
db/
  init.sql
docker-compose.yml
Dockerfile
```

## Environment

Copy `.env.example` to `.env` and update:

```env
BOT_TOKEN=...
DATABASE_URL=postgresql://phusar:phusar@postgres:5432/phusar
REDIS_URL=redis://redis:6379/0
ADMIN_IDS=111111111
DEFAULT_LANGUAGE=en

# Optional premium module (only used when PREMIUM_ENABLED=true)
PREMIUM_ENABLED=false
PAYMENT_PHONE=09XXXXXXXXX
KBZPAY_QR_FILE_ID=
WAVEMONEY_QR_FILE_ID=
```

## Run with Docker

```bash
docker compose up --build
```

## Run Locally

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

## Admin Commands

- `/ban <user_id>`
- `/unban <user_id>`

When premium is enabled, `/approve <user_id> <days>` and `/reject <user_id>` are also available.
