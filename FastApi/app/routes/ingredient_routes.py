from schemas.ingredient_schema import Ingredient
from database import IngredientModel, IngredientCategoryModel, UnitModel
from fastapi import APIRouter, Body, HTTPException

ingredient_route = APIRouter()

@ingredient_route.post("/")
async def create_ingredient(ingredient: Ingredient = Body(...)):
    """Create a new ingredient."""
    try:
        IngredientCategoryModel.get(IngredientCategoryModel.id == ingredient.category_id)
        UnitModel.get(UnitModel.id == ingredient.unit_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Category or unit not found") from exc

    IngredientModel.create(
        name=ingredient.name,
        category_id=ingredient.category_id,
        unit_id=ingredient.unit_id
    )
    return {"message": "Ingredient created successfully"}

@ingredient_route.get("/")
async def read_all_ingredients():
    """Retrieve a list of all ingredients."""
    ingredients = IngredientModel.select().dicts()
    return list(ingredients)

@ingredient_route.get("/{ingredient_id}")
async def read_ingredient(ingredient_id: int):
    """Retrieve a specific ingredient by its ID."""
    try:
        ingredient = IngredientModel.get(IngredientModel.id == ingredient_id)
        return ingredient
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Ingredient not found") from exc

@ingredient_route.put("/{ingredient_id}")
async def update_ingredient(ingredient_id: int, ingredient: Ingredient = Body(...)):
    """Update an existing ingredient."""
    try:
        existing_ingredient = IngredientModel.get(IngredientModel.id == ingredient_id)
        existing_ingredient.name = ingredient.name
        existing_ingredient.category_id = ingredient.category_id
        existing_ingredient.unit_id = ingredient.unit_id
        existing_ingredient.save()
        return {"message": "Ingredient updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Ingredient not found") from exc

@ingredient_route.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: int):
    """Delete an ingredient by its ID."""
    rows_deleted = IngredientModel.delete().where(IngredientModel.id == ingredient_id).execute()
    if rows_deleted:
        return {"message": "Ingredient deleted successfully"}
    raise HTTPException(status_code=404, detail="Ingredient not found")
