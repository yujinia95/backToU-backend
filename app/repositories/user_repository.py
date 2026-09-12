# Type annotations for flexible dictionary value types
from typing import Any

# PostgreSQL database driver for connection and query management
from psycopg import Connection


class UserRepository:
    """
    Data access layer for user entities.

    Encapsulates database operations for the 'users' table, including
    querying existing records and persisting newly created users.
    """

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        """Fetch a user row by email, or return None."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, first_name, last_name, password_hash, created_at
                FROM users
                WHERE email = %s
                """,
                (email,), # Parameterized query to prevent SQL injection
            )
            return cursor.fetchone()
        

    def create_user(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
    ) -> dict[str, Any]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (email, first_name, last_name, password_hash)
                VALUES (%s, %s, %s, %s)
                RETURNING id, email, first_name, last_name
                """,
                (email, first_name, last_name, password_hash),
            )
            created_user = cursor.fetchone()

        if created_user is None:
            raise RuntimeError("Database did not return the created user")

        return created_user
