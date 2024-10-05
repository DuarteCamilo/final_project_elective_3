from pydantic import BaseModel

class RecipeIngredient(BaseModel):
    """Model representing an ingredient in a recipe."""
    recipe_id: int
    ingredient_id: int
    quantity: float
    unit: str
