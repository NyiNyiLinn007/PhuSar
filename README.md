# Phu Sar (ဖူးစာ) Telegram Dating Bot

Production-ready starter for a Myanmar-focused Telegram dating bot built with `aiogram 3.x`, PostgreSQL, and Redis.

## Features

- FSM registration flow:
  - Language selection (English / Unicode Burmese)
  - Gender + seeking preferences
  - Region + township
  - Age, bio, photo upload validation
- Discovery engine:
  - Candidate filtering by seeking preference
  - Actions: `Like`, `Pass`, `SuperLike`
  - Mutual-like match notifications
- Premium flow:
  - KBZPay / WaveMoney screenshot upload
  - Admin approval/rejection callbacks
- Moderation:
  - In-app report button on each profile
  - Admin review and one-click ban workflow
- Deployment:
  - Docker + `docker-compose` with PostgreSQL and Redis

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
ADMIN_IDS=111111111,222222222
DEFAULT_LANGUAGE=en
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

Premium approvals and report moderation are handled with inline admin buttons.
