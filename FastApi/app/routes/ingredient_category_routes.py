from schemas.ingredient_category_schema import IngredientCategory
from database import IngredientCategoryModel
from fastapi import APIRouter, Body, HTTPException

ingredient_category_route = APIRouter()

@ingredient_category_route.post("/")
async def create_ingredient_category(ingredientCategory: IngredientCategory = Body(...)):
    """Create a new ingredient category."""
    IngredientCategoryModel.create(name=ingredientCategory.name)
    return {"message": "Ingredient category created successfully"}

@ingredient_category_route.get("/")
async def read_all_ingredient_categories():
    """Retrieve a list of all ingredient categories."""
    categories = IngredientCategoryModel.select().dicts()
    return list(categories)

@ingredient_category_route.get("/{category_id}")
async def read_ingredient_category(category_id: int):
    """Retrieve a specific ingredient category by its ID."""
    try:
        category = IngredientCategoryModel.get(IngredientCategoryModel.id == category_id)
        return category
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Category not found") from exc

@ingredient_category_route.put("/{category_id}")
async def update_ingredient_category(category_id: int, category: IngredientCategory = Body(...)):
    """Update an existing ingredient category."""
    try:
        existing_category = IngredientCategoryModel.get(IngredientCategoryModel.id == category_id)
        existing_category.name = category.name
        existing_category.save()
        return {"message": "Category updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Category not found") from exc

@ingredient_category_route.delete("/{category_id}")
async def delete_ingredient_category(category_id: int):
    """Delete an ingredient category by its ID."""
    rows_deleted = IngredientCategoryModel.delete().where(IngredientCategoryModel.id == category_id).execute()
    if rows_deleted:
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")
