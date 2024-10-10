from pydantic import BaseModel

class PantryItem(BaseModel):
    """Model representing an item in the pantry."""
    id: int
    quantity: float
    unit_id: int
    expiry_date: str
    user_id: int
    ingredient_id: int
