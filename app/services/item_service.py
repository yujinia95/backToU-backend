from app.schemas.item import ItemResponse, ItemPostRequest, ItemUpdateRequest
from app.models.item import POST_NEW_ITEM, GET_ALL_ITEMS, GET_ITEM_BY_ID, DELETE_ITEM_BY_ID
from app.database import connection
from typing import List

def create_item(data: ItemPostRequest) -> ItemResponse:
    cursor = connection.cursor()
    try:
        cursor.execute(
            POST_NEW_ITEM, 
            (data.user_id, data.type, data.date, data.title, data.description, data.category, data.colors, data.brand, data.location)
        )
        
        item_id, user_id, type_, status, date_, title, description, category, colors, brand, location, created_at = cursor.fetchone()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    
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

def update_item(id: int, data: ItemUpdateRequest) -> ItemResponse:
    updated_data = data.model_dump(exclude_unset=True)
    set_clauses = [f"{field} = %s" for field in updated_data.keys()]
    set_clause_str=", ".join(set_clauses)
    
    query = f"""
        UPDATE items
        SET {set_clause_str}
        WHERE id = %s
        RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
    """
    
    cursor = connection.cursor()
    try:
        cursor.execute(query, (list(updated_data.values())+ [id]))
        row = cursor.fetchone()

        if row is None:
            raise ValueError("Item is not found")
        
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    
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

def delete_item(item_id: int) -> None:
    cursor = connection.cursor()
    try: 
        cursor.execute(DELETE_ITEM_BY_ID, (item_id,))
        if cursor.rowcount == 0:
            raise ValueError("Item is not found")
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
