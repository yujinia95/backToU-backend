from datetime import datetime

from psycopg import Connection
from psycopg.errors import ForeignKeyViolation

from app.repositories.item_repository import ItemRepository
from app.exceptions.item import EmptyUpdateError, ItemNotFoundError, UserNotFoundError, InvalidUpdateError
from app.schemas.item import ItemDetailResponse, ItemResponse, ItemPostRequest, ItemStatus, ItemUpdateRequest
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

    def get_item_by_id(self, item_id: int) -> ItemDetailResponse:
        row = self.item_repository.get_by_id(item_id)
        if row is None:
            raise ItemNotFoundError("Item not found.")
        return ItemDetailResponse(
            **row,
            poster={
                "id": row["poster_id"],
                "first_name": row["poster_first_name"],
                "last_name": row["poster_last_name"],
            },
        )

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

        # returned_at is owned by the server: stamped when an item becomes
        # "returned", cleared when it moves back to any other status. A database
        # constraint keeps the two in step, so a returned item always has a date.
        if "status" in update_data:
            update_data["returned_at"] = (
                datetime.now() if update_data["status"] == ItemStatus.RETURNED else None
            )

        set_clauses = []
        values = []
        for field, value in update_data.items():
            if field == "returned_at" and value is not None:
                # Re-sending status="returned" must not rewrite the date the
                # item actually went back, so only an empty column is filled.
                set_clauses.append("returned_at = COALESCE(returned_at, %s)")
            else:
                set_clauses.append(f"{field} = %s")
            values.append(value)

        set_clause_str = ", ".join(set_clauses)

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
