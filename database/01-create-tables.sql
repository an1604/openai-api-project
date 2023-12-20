    CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    conversation_obj BYTEA,
    history TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id TEXT,
    user_input TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE requests (
    conversation_id TEXT PRIMARY KEY,
    request_id TEXT
);

CREATE TABLE customers (
    id TEXT PRIMARY KEY,
    customer_name TEXT,
    max_cd INT,
    gender CHAR(6)
);
