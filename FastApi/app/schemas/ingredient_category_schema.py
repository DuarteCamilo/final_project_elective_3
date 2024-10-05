from pydantic import BaseModel

class IngredientCategory(BaseModel):
    """Model representing an ingredient category."""
    id: int
    name: str
