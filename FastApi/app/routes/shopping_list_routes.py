from schemas.shopping_list_schema import ShoppingList
from database import ShoppingListModel
from fastapi import APIRouter, Body, HTTPException

shopping_list_route = APIRouter()

@shopping_list_route.post("/")
async def create_shopping_list(shopping_list: ShoppingList = Body(...)):
    """Create a new shopping list."""
    ShoppingListModel.create(
        name=shopping_list.name,
        created_at=shopping_list.created_at,
        user_id=shopping_list.user_id
    )
    return {"message": "Shopping list created successfully"}

@shopping_list_route.get("/")
async def read_all_shopping_lists():
    """Retrieve a list of all shopping lists."""
    shopping_lists = ShoppingListModel.select().dicts()
    return list(shopping_lists)

@shopping_list_route.get("/{shopping_list_id}")
async def read_shopping_list(shopping_list_id: int):
    """Retrieve a specific shopping list by its ID."""
    try:
        shopping_list = ShoppingListModel.get(ShoppingListModel.id == shopping_list_id)
        return shopping_list
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Shopping list not found") from exc

@shopping_list_route.put("/{shopping_list_id}")
async def update_shopping_list(shopping_list_id: int, shopping_list: ShoppingList = Body(...)):
    """Update an existing shopping list."""
    try:
        existing_list = ShoppingListModel.get(ShoppingListModel.id == shopping_list_id)
        existing_list.name = shopping_list.name
        existing_list.created_at = shopping_list.created_at
        existing_list.user_id = shopping_list.user_id
        existing_list.save()
        return {"message": "Shopping list updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Shopping list not found") from exc

@shopping_list_route.delete("/{shopping_list_id}")
async def delete_shopping_list(shopping_list_id: int):
    """Delete a shopping list by its ID."""
    rows_deleted = ShoppingListModel.delete().where(ShoppingListModel.id == shopping_list_id).execute()
    if rows_deleted:
        return {"message": "Shopping list deleted successfully"}
    raise HTTPException(status_code=404, detail="Shopping list not found")
