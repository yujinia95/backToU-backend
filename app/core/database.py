# psycopg: the driver that connects Python to PostgreSQL.
# dict_row: returns each row as a dictionary like {"email": "..."}.
import psycopg
from psycopg.rows import dict_row

from app.core.config import settings

# Creates PostgreSQL connections.
class Database:
    def connect(self):
        return psycopg.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password or None,  # None if no password
            dbname=settings.db_name,
            row_factory=dict_row,
        )

# Shared instance used across the app.
database = Database()


# Provide one connection per request, and always close it after.
def get_db():
    conn = database.connect()  # 1. Open a connection
    try:
        yield conn             # 2. Pass it to the route and wait
    finally:
        conn.close()           # 3. Close it when the request is done
