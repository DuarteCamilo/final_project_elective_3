from schemas.recipe_recipe_type_schema import RecipeRecipeType
from database import RecipeRecipeTypeModel
from fastapi import APIRouter, Body, HTTPException

recipe_recipe_type_route = APIRouter()

@recipe_recipe_type_route.post("/")
async def create_recipe_recipe_type(recipe_recipe_type: RecipeRecipeType = Body(...)):
    """Create a new recipe-type relationship."""
    RecipeRecipeTypeModel.create(
        recipe_id=recipe_recipe_type.recipe_id,
        recipe_type_id=recipe_recipe_type.recipe_type_id
    )
    return {"message": "Recipe type assigned successfully"}

@recipe_recipe_type_route.get("/")
async def read_all_recipe_recipe_types():
    """Retrieve a list of all recipe-type relationships."""
    recipe_recipe_types = RecipeRecipeTypeModel.select().dicts()
    return list(recipe_recipe_types)

@recipe_recipe_type_route.get("/{recipe_recipe_type_id}")
async def read_recipe_recipe_type(recipe_recipe_type_id: int):
    """Retrieve a specific recipe-type relationship by its ID."""
    try:
        recipe_recipe_type = RecipeRecipeTypeModel.get(RecipeRecipeTypeModel.id == recipe_recipe_type_id)
        return recipe_recipe_type
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe-type relationship not found") from exc

@recipe_recipe_type_route.delete("/{recipe_recipe_type_id}")
async def delete_recipe_recipe_type(recipe_recipe_type_id: int):
    """Delete a recipe-type relationship by its ID."""
    rows_deleted = RecipeRecipeTypeModel.delete().where(RecipeRecipeTypeModel.id == recipe_recipe_type_id).execute()
    if rows_deleted:
        return {"message": "Recipe-type relationship deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe-type relationship not found")
