from pydantic import BaseModel

class RecipeType(BaseModel):
    """Model representing a recipe type."""
    id: int
    name: str
