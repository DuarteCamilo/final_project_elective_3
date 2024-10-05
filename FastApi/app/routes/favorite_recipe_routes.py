from schemas.favorite_recipe_schema import FavoriteRecipe
from database import FavoriteRecipeModel
from fastapi import APIRouter, Body, HTTPException

favorite_recipe_route = APIRouter()

@favorite_recipe_route.post("/")
async def create_favorite_recipe(favorite_recipe: FavoriteRecipe = Body(...)):
    """Create a new favorite recipe for a user."""
    FavoriteRecipeModel.create(
        user_id=favorite_recipe.user_id,
        recipe_id=favorite_recipe.recipe_id
    )
    return {"message": "Favorite recipe added successfully"}

@favorite_recipe_route.get("/")
async def read_all_favorite_recipes():
    """Retrieve a list of all favorite recipes."""
    favorite_recipes = FavoriteRecipeModel.select().dicts()
    return list(favorite_recipes)

@favorite_recipe_route.get("/{favorite_recipe_id}")
async def read_favorite_recipe(favorite_recipe_id: int):
    """Retrieve a specific favorite recipe by its ID."""
    try:
        favorite_recipe = FavoriteRecipeModel.get(FavoriteRecipeModel.id == favorite_recipe_id)
        return favorite_recipe
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Favorite recipe not found") from exc

@favorite_recipe_route.delete("/{favorite_recipe_id}")
async def delete_favorite_recipe(favorite_recipe_id: int):
    """Delete a favorite recipe by its ID."""
    rows_deleted = FavoriteRecipeModel.delete().where(FavoriteRecipeModel.id == favorite_recipe_id).execute()
    if rows_deleted:
        return {"message": "Favorite recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Favorite recipe not found")
