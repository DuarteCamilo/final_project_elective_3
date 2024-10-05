from pydantic import BaseModel

class ShoppingList(BaseModel):
    """Model representing a shopping list."""
    id: int
    name: str
    created_at: str
    user_id: int
