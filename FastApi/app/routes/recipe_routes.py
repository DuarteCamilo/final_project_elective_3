from schemas.recipe_schema import Recipe
from database import RecipeModel
from fastapi import APIRouter, Body, HTTPException

recipe_route = APIRouter()

@recipe_route.post("/")
async def create_recipe(recipe: Recipe = Body(...)):
    """Create a new recipe."""
    RecipeModel.create(
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        preparation_time=recipe.preparation_time,
        datosNutricionales=recipe.datosNutricionales,
        type_id=recipe.type_id,
        difficulty=recipe.difficulty,
        is_public=recipe.is_public,
        user_id=recipe.user_id
    )
    return {"message": "Recipe created successfully"}

@recipe_route.get("/")
async def read_all_recipes():
    """Retrieve a list of all recipes."""
    recipes = RecipeModel.select().dicts()
    return list(recipes)

@recipe_route.get("/{recipe_id}")
async def read_recipe(recipe_id: int):
    """Retrieve a specific recipe by its ID."""
    try:
        recipe = RecipeModel.get(RecipeModel.id == recipe_id)
        return recipe
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe not found") from exc

@recipe_route.put("/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: Recipe = Body(...)):
    """Update an existing recipe."""
    try:
        existing_recipe = RecipeModel.get(RecipeModel.id == recipe_id)
        return existing_recipe
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe not actualized") from exc