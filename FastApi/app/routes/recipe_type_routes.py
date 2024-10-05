from schemas.recipe_type_schema import RecipeType
from database import RecipeTypeModel
from fastapi import APIRouter, Body, HTTPException

recipe_type_route = APIRouter()

@recipe_type_route.post("/")
async def create_recipe_type(recipe_type: RecipeType = Body(...)):
    """Create a new recipe type."""
    RecipeTypeModel.create(name=recipe_type.name)
    return {"message": "Recipe type created successfully"}

@recipe_type_route.get("/")
async def read_all_recipe_types():
    """Retrieve a list of all recipe types."""
    recipe_types = RecipeTypeModel.select().dicts()
    return list(recipe_types)

@recipe_type_route.get("/{recipe_type_id}")
async def read_recipe_type(recipe_type_id: int):
    """Retrieve a specific recipe type by its ID."""
    try:
        recipe_type = RecipeTypeModel.get(RecipeTypeModel.id == recipe_type_id)
        return recipe_type
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe type not found") from exc

@recipe_type_route.put("/{recipe_type_id}")
async def update_recipe_type(recipe_type_id: int, recipe_type: RecipeType = Body(...)):
    """Update an existing recipe type."""
    try:
        existing_recipe_type = RecipeTypeModel.get(RecipeTypeModel.id == recipe_type_id)
        existing_recipe_type.name = recipe_type.name
        existing_recipe_type.save()
        return {"message": "Recipe type updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Recipe type not found") from exc

@recipe_type_route.delete("/{recipe_type_id}")
async def delete_recipe_type(recipe_type_id: int):
    """Delete a recipe type by its ID."""
    rows_deleted = RecipeTypeModel.delete().where(RecipeTypeModel.id == recipe_type_id).execute()
    if rows_deleted:
        return {"message": "Recipe type deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe type not found")
