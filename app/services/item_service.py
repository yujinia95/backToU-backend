from psycopg import Connection
from psycopg.errors import ForeignKeyViolation

from app.repositories.item_repository import ItemRepository
from app.exceptions.item import EmptyUpdateError, ItemNotFoundError, UserNotFoundError, InvalidUpdateError
from app.schemas.item import ItemResponse, ItemPostRequest, ItemUpdateRequest
from typing import List

NOT_NULLABLE_FIELDS = {
    "type",
    "status",
    "date",
    "title",
    "category",
    "colors",
    "location",
}

class ItemService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.item_repository = ItemRepository(self.conn)

    def create_item(self, data: ItemPostRequest) -> ItemResponse:
        try:
            row = self.item_repository.create(
                user_id=data.user_id,
                type_=data.type,
                date_=data.date,
                title=data.title,
                description=data.description,
                category=data.category,
                colors=data.colors,
                brand=data.brand,
                location=data.location,
            )
            self.conn.commit()
        except ForeignKeyViolation as error:
            self.conn.rollback()
            raise UserNotFoundError("User with the given user_id does not exist.") from error
        except Exception:
            self.conn.rollback()
            raise

        return ItemResponse(**row)

    def get_item_by_id(self, item_id: int) -> ItemResponse:
        row = self.item_repository.get_by_id(item_id)
        if row is None:
            raise ItemNotFoundError("Item not found.")
        return ItemResponse(**row)

    def get_all_items(self) -> List[ItemResponse]:
        rows = self.item_repository.get_all()
        return [ItemResponse(**row) for row in rows]

    def update_item(self, item_id: int, data: ItemUpdateRequest) -> ItemResponse:
        update_data = data.model_dump(exclude_unset=True)
        
        for field in NOT_NULLABLE_FIELDS:
            if field in update_data and update_data[field] is None:
                raise InvalidUpdateError(f"{field} cannot be set to null.")

        if not update_data:
            raise EmptyUpdateError("No fields provided to update.")

        set_clauses = [f"{field} = %s" for field in update_data.keys()]
        set_clause_str = ", ".join(set_clauses)
        values = list(update_data.values())

        try:
            row = self.item_repository.update(item_id, set_clause_str, values)
            if row is None:
                raise ItemNotFoundError("Item not found.")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        return ItemResponse(**row)

    def delete_item(self, item_id: int) -> None:
        try:
            affected = self.item_repository.delete(item_id)
            if affected == 0:
                raise ItemNotFoundError("Item not found.")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
