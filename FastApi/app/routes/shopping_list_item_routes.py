from schemas.shopping_list_item_schema import ShoppingListItem
from database import ShoppingListItemModel
from fastapi import APIRouter, Body, HTTPException

shopping_list_item_route = APIRouter()

@shopping_list_item_route.post("/")
async def create_shopping_list_item(shopping_list_item: ShoppingListItem = Body(...)):
    """Create a new shopping list item."""
    ShoppingListItemModel.create(
        shopping_list_id=shopping_list_item.shopping_list_id,
        ingredient_id=shopping_list_item.ingredient_id,
        quantity=shopping_list_item.quantity,
        unit=shopping_list_item.unit,
        is_purchased=shopping_list_item.is_purchased
    )
    return {"message": "Shopping list item created successfully"}

@shopping_list_item_route.get("/")
async def read_all_shopping_list_items():
    """Retrieve a list of all shopping list items."""
    items = ShoppingListItemModel.select().dicts()
    return list(items)

@shopping_list_item_route.get("/{item_id}")
async def read_shopping_list_item(item_id: int):
    """Retrieve a specific shopping list item by its ID."""
    try:
        item = ShoppingListItemModel.get(ShoppingListItemModel.id == item_id)
        return item
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Shopping list item not found") from exc

@shopping_list_item_route.put("/{item_id}")
async def update_shopping_list_item(item_id: int, shopping_list_item: ShoppingListItem = Body(...)):
    """Update an existing shopping list item."""
    try:
        existing_item = ShoppingListItemModel.get(ShoppingListItemModel.id == item_id)
        existing_item.shopping_list_id = shopping_list_item.shopping_list_id
        existing_item.ingredient_id = shopping_list_item.ingredient_id
        existing_item.quantity = shopping_list_item.quantity
        existing_item.unit = shopping_list_item.unit
        existing_item.is_purchased = shopping_list_item.is_purchased
        existing_item.save()
        return {"message": "Shopping list item updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Shopping list item not found") from exc

@shopping_list_item_route.delete("/{item_id}")
async def delete_shopping_list_item(item_id: int):
    """Delete a shopping list item by its ID."""
    rows_deleted = ShoppingListItemModel.delete().where(ShoppingListItemModel.id == item_id).execute()
    if rows_deleted:
        return {"message": "Shopping list item deleted successfully"}
    raise HTTPException(status_code=404, detail="Shopping list item not found")

