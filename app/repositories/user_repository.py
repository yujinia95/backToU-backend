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
        """Initialize the repository with a database connection."""
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
                (email,),  # Parameterized query to prevent SQL injection
            )
            return cursor.fetchone()

    def create_user(
        self,
        *,  # Require the following arguments to be passed by name
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
    ) -> dict[str, Any]:
        """Insert a user row and return its public fields."""
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
    
    def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        """Fetch an user by id, or return None."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    i.id,
                    i.user_id,
                    i.type,
                    i.status,
                    i.date,
                    i.title,
                    i.description,
                    i.category,
                    i.colors,
                    i.brand,
                    i.location,
                    i.created_at,
                    i.returned_at,
                    u.id AS poster_id,
                    u.first_name AS poster_first_name,
                    u.last_name AS poster_last_name
                FROM items AS i
                JOIN users AS u ON u.id = i.user_id
                WHERE i.id = %s
                """,
                (item_id,),
            )
            return cursor.fetchone()
