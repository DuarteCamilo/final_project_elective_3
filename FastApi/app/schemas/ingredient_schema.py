from pydantic import BaseModel

class Ingredient(BaseModel):
    """Model representing an ingredient."""
    id: int
    name: str
    category_id: int
    unit_id: int