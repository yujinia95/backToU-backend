CREATE_USERS_TABLE = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
"""

INSERT_USER = """
    INSERT INTO users (first_name, last_name, email, password)
    VALUES (%s, %s, %s, %s)
    RETURNING id, first_name, last_name, email;
"""

LOGIN_USER = """
    SELECT id, first_name, last_name, email, password
    FROM users
    WHERE email = %s
"""
