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

# provide user_id since we don't have JWT yet
POST_NEW_ITEM = """
    INSERT INTO items (user_id, type, date, title, description, category, colors, brand, location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
"""

GET_ALL_ITEMS = """
    SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
    FROM items
"""

GET_ITEM_BY_ID = """
    SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
    FROM items
    WHERE id = %s
"""

DELETE_ITEM_BY_ID = """
    DELETE FROM items
    WHERE id = %s;  
"""

