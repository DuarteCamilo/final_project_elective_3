from schemas.pantry_item_schema import PantryItem
from database import PantryItemModel
from fastapi import APIRouter, Body, HTTPException

pantry_item_route = APIRouter()

@pantry_item_route.post("/")
async def create_pantry_item(pantry_item: PantryItem = Body(...)):
    """Create a new pantry item."""
    PantryItemModel.create(
        user_id=pantry_item.user_id,
        ingredient_id=pantry_item.ingredient_id,
        quantity=pantry_item.quantity
    )
    return {"message": "Pantry item created successfully"}

@pantry_item_route.get("/")
async def read_all_pantry_items():
    """Retrieve a list of all pantry items."""
    pantry_items = PantryItemModel.select().dicts()
    return list(pantry_items)

@pantry_item_route.get("/{pantry_item_id}")
async def read_pantry_item(pantry_item_id: int):
    """Retrieve a specific pantry item by its ID."""
    try:
        pantry_item = PantryItemModel.get(PantryItemModel.id == pantry_item_id)
        return pantry_item
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Pantry item not found") from exc

@pantry_item_route.put("/{pantry_item_id}")
async def update_pantry_item(pantry_item_id: int, pantry_item: PantryItem = Body(...)):
    """Update an existing pantry item."""
    try:
        existing_pantry_item = PantryItemModel.get(PantryItemModel.id == pantry_item_id)
        existing_pantry_item.user_id = pantry_item.user_id
        existing_pantry_item.ingredient_id = pantry_item.ingredient_id
        existing_pantry_item.quantity = pantry_item.quantity
        existing_pantry_item.save()
        return {"message": "Pantry item updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Pantry item not found") from exc

@pantry_item_route.delete("/{pantry_item_id}")
async def delete_pantry_item(pantry_item_id: int):
    """Delete a pantry item by its ID."""
    rows_deleted = PantryItemModel.delete().where(PantryItemModel.id == pantry_item_id).execute()
    if rows_deleted:
        return {"message": "Pantry item deleted successfully"}
    raise HTTPException(status_code=404, detail="Pantry item not found")
