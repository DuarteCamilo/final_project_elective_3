from schemas.menu_recipe_schema import MenuRecipe
from database import MenuRecipeModel
from fastapi import APIRouter, Body, HTTPException

menu_recipe_route = APIRouter()

@menu_recipe_route.post("/")
async def create_menu_recipe(menu_recipe: MenuRecipe = Body(...)):
    """Create a new recipe in a menu."""
    MenuRecipeModel.create(
        menu_id=menu_recipe.menu_id,
        recipe_id=menu_recipe.recipe_id,
        meal_time=menu_recipe.meal_time,
        planned_date=menu_recipe.planned_date
    )
    return {"message": "Menu recipe created successfully"}

@menu_recipe_route.get("/")
async def read_all_menu_recipes():
    """Retrieve a list of all menu recipes."""
    menu_recipes = MenuRecipeModel.select().dicts()
    return list(menu_recipes)

@menu_recipe_route.get("/{menu_recipe_id}")
async def read_menu_recipe(menu_recipe_id: int):
    """Retrieve a specific menu recipe by its ID."""
    try:
        menu_recipe = MenuRecipeModel.get(MenuRecipeModel.id == menu_recipe_id)
        return menu_recipe
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Menu recipe not found") from exc

@menu_recipe_route.put("/{menu_recipe_id}")
async def update_menu_recipe(menu_recipe_id: int, menu_recipe: MenuRecipe = Body(...)):
    """Update an existing menu recipe."""
    try:
        existing_menu_recipe = MenuRecipeModel.get(MenuRecipeModel.id == menu_recipe_id)
        existing_menu_recipe.menu_id = menu_recipe.menu_id
        existing_menu_recipe.recipe_id = menu_recipe.recipe_id
        existing_menu_recipe.meal_time = menu_recipe.meal_time
        existing_menu_recipe.planned_date = menu_recipe.planned_date
        existing_menu_recipe.save()
        return {"message": "Menu recipe updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Menu recipe not found") from exc

@menu_recipe_route.delete("/{menu_recipe_id}")
async def delete_menu_recipe(menu_recipe_id: int):
    """Delete a menu recipe by its ID."""
    rows_deleted = MenuRecipeModel.delete().where(MenuRecipeModel.id == menu_recipe_id).execute()
    if rows_deleted:
        return {"message": "Menu recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Menu recipe not found")
