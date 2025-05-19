CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tg_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    full_name TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    inviter_id BIGINT,
    points INTEGER DEFAULT 0,
    badge TEXT DEFAULT 'none',
    level INTEGER DEFAULT 1,
    referral_link TEXT,
    is_banned BOOLEAN DEFAULT FALSE,
    suspicious BOOLEAN DEFAULT FALSE,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE referrals (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    referred_tg_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    successful BOOLEAN DEFAULT FALSE
);

CREATE TABLE events_log (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    event_type TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE challenges (
    id SERIAL PRIMARY KEY,
    description TEXT,
    type TEXT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE challenge_participation (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    challenge_id INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP
);

CREATE TABLE admin_actions (
    id SERIAL PRIMARY KEY,
    admin_id BIGINT,
    action TEXT,
    target_user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cheat_reports (
    id SERIAL PRIMARY KEY,
    reported_user_id BIGINT,
    reporter_id BIGINT,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
