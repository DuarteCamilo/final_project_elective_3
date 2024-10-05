from schemas.menu_schema import Menu
from database import MenuModel
from fastapi import APIRouter, Body, HTTPException

menu_route = APIRouter()

@menu_route.post("/")
async def create_menu(menu: Menu = Body(...)):
    """Create a new menu."""
    MenuModel.create(name=menu.name, user_id=menu.user_id)
    return {"message": "Menu created successfully"}

@menu_route.get("/")
async def read_all_menus():
    """Retrieve a list of all menus."""
    menus = MenuModel.select().dicts()
    return list(menus)

@menu_route.get("/{menu_id}")
async def read_menu(menu_id: int):
    """Retrieve a specific menu by its ID."""
    try:
        menu = MenuModel.get(MenuModel.id == menu_id)
        return menu
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Menu not found") from exc

@menu_route.put("/{menu_id}")
async def update_menu(menu_id: int, menu: Menu = Body(...)):
    """Update an existing menu."""
    try:
        existing_menu = MenuModel.get(MenuModel.id == menu_id)
        existing_menu.name = menu.name
        existing_menu.user_id = menu.user_id
        existing_menu.save()
        return {"message": "Menu updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Menu not found") from exc

@menu_route.delete("/{menu_id}")
async def delete_menu(menu_id: int):
    """Delete a menu by its ID."""
    rows_deleted = MenuModel.delete().where(MenuModel.id == menu_id).execute()
    if rows_deleted:
        return {"message": "Menu deleted successfully"}
    raise HTTPException(status_code=404, detail="Menu not found")
