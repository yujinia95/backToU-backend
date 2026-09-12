CREATE_ITEM_TABLE = """
    CREATE TABLE items (
        id BIGSERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        type VARCHAR(20) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'active',
        date DATE NOT NULL,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        colors VARCHAR(20)[],
        brand VARCHAR(100),
        location TEXT NOT NULL,
        image_key BYTEA,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
"""
