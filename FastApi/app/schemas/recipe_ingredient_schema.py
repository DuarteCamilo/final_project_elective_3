from pydantic import BaseModel

class RecipeIngredient(BaseModel):
    """Model representing an ingredient in a recipe."""
    id: int
    recipe_id: int
    ingredient_id: int
    quantity: float
    unit_id: int
