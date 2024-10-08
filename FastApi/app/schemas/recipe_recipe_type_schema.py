from pydantic import BaseModel

class RecipeRecipeType(BaseModel):
    """Model representing a relationship between recipe and recipe type."""
    id : int
    recipe_id: int
    type_id: int
