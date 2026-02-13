CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    full_name VARCHAR(100),
    username VARCHAR(64),
    language VARCHAR(5) DEFAULT 'en',
    age INTEGER CHECK (age >= 18 AND age <= 99),
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')),
    seeking VARCHAR(10) CHECK (seeking IN ('male', 'female', 'both')),
    location_region VARCHAR(50),
    township VARCHAR(50),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    bio TEXT,
    photo_id TEXT,
    is_premium BOOLEAN DEFAULT FALSE,
    premium_until TIMESTAMP,
    likes_today INTEGER DEFAULT 0,
    likes_reset_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_banned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actions (
    actor_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    target_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    action_type VARCHAR(10) CHECK (action_type IN ('like', 'dislike', 'superlike')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (actor_id, target_id)
);

CREATE TABLE IF NOT EXISTS premium_requests (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider VARCHAR(20) NOT NULL CHECK (provider IN ('kbzpay', 'wavemoney')),
    plan_code VARCHAR(20) NOT NULL DEFAULT 'weekly' CHECK (plan_code IN ('weekly', 'monthly')),
    duration_days INTEGER NOT NULL DEFAULT 7 CHECK (duration_days IN (7, 30)),
    price_mmk INTEGER NOT NULL DEFAULT 1500 CHECK (price_mmk IN (1500, 3000)),
    screenshot_file_id TEXT NOT NULL,
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    reviewed_by BIGINT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id BIGSERIAL PRIMARY KEY,
    reporter_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    target_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    reason VARCHAR(30) NOT NULL,
    status VARCHAR(15) DEFAULT 'pending' CHECK (status IN ('pending', 'dismissed', 'banned')),
    reviewed_by BIGINT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_match_fields ON users (gender, seeking, is_banned);
CREATE INDEX IF NOT EXISTS idx_actions_target ON actions (target_id);
CREATE INDEX IF NOT EXISTS idx_premium_requests_status ON premium_requests (status);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports (status);

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS premium_until TIMESTAMP;
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS likes_today INTEGER DEFAULT 0;
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS likes_reset_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION;
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION;
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS username VARCHAR(64);
ALTER TABLE premium_requests
    ADD COLUMN IF NOT EXISTS plan_code VARCHAR(20) DEFAULT 'weekly';
ALTER TABLE premium_requests
    ADD COLUMN IF NOT EXISTS duration_days INTEGER DEFAULT 7;
ALTER TABLE premium_requests
    ADD COLUMN IF NOT EXISTS price_mmk INTEGER DEFAULT 1500;
