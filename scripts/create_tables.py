from app.database import connection
from app.models.user import CREATE_USERS_TABLE
from app.models.item import CREATE_ITEM_TABLE

cursor = connection.cursor()
cursor.execute(CREATE_ITEM_TABLE)
cursor.execute(CREATE_USERS_TABLE)
connection.commit()
print("Tables created.")
