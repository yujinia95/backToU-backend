from app.schemas.item import ItemResponse
from app.models.item import GET_ALL_ITEMS, GET_ITEM_BY_ID
from app.database import connection
from typing import List

def get_item_by_id(id: int) -> ItemResponse:
    cursor = connection.cursor()
    cursor.execute(GET_ITEM_BY_ID, (id,))
    row = cursor.fetchone()

    if row is None:
        raise ValueError("Item is not found")
    
    item_id, user_id, type_, status, date_, title, description, category, colors, brand, location, created_at = row
    
    return ItemResponse(
        id=item_id,
        user_id=user_id,
        type=type_,
        status=status,
        date=date_,
        title=title,
        description=description,
        category=category,
        colors=colors,
        brand=brand,
        location=location,
        created_at=created_at
    )


def get_all_items() -> List[ItemResponse]:
    cursor = connection.cursor()
    cursor.execute(GET_ALL_ITEMS)
    rows = cursor.fetchall() 

    items = [] 
    for row in rows:
        item_id, user_id, type_, status, date_, title, description, category, colors, brand, location, created_at = row
        items.append(ItemResponse(
            id=item_id,
            user_id=user_id,
            type=type_,
            status=status,
            date=date_,
            title=title,
            description=description,
            category=category,
            colors=colors,
            brand=brand,
            location=location,
            created_at=created_at
        ))

    return items
