from schemas.recipe_ingredient_schema import RecipeIngredient
from database import RecipeIngredientModel, RecipeModel, IngredientModel
from fastapi import APIRouter, Body, HTTPException

recipe_ingredient_route = APIRouter()

@recipe_ingredient_route.post("/")
async def create_recipe_ingredient(recipe_ingredient: RecipeIngredient = Body(...)):
    """Add an ingredient to a recipe."""
    try:
        RecipeModel.get(RecipeModel.id == recipe_ingredient.recipe_id)
        IngredientModel.get(IngredientModel.id == recipe_ingredient.ingredient_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe or ingredient not found") from exc

    RecipeIngredientModel.create(
        recipe_id=recipe_ingredient.recipe_id,
        ingredient_id=recipe_ingredient.ingredient_id,
        quantity=recipe_ingredient.quantity
    )
    return {"message": "Ingredient added to recipe successfully"}

@recipe_ingredient_route.get("/")
async def read_all_recipe_ingredients():
    """Retrieve a list of all recipe ingredients."""
    recipe_ingredients = RecipeIngredientModel.select().dicts()
    return list(recipe_ingredients)

@recipe_ingredient_route.get("/{recipe_ingredient_id}")
async def read_recipe_ingredient(recipe_ingredient_id: int):
    """Retrieve a specific recipe ingredient by its ID."""
    try:
        recipe_ingredient = RecipeIngredientModel.get(RecipeIngredientModel.id == recipe_ingredient_id)
        return recipe_ingredient
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe ingredient not found") from exc

@recipe_ingredient_route.delete("/{recipe_ingredient_id}")
async def delete_recipe_ingredient(recipe_ingredient_id: int):
    """Remove an ingredient from a recipe by its ID."""
    rows_deleted = RecipeIngredientModel.delete().where(RecipeIngredientModel.id == recipe_ingredient_id).execute()
    if rows_deleted:
        return {"message": "Recipe ingredient deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe ingredient not found")
