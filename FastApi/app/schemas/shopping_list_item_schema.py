from pydantic import BaseModel

class ShoppingListItem(BaseModel):
    """Model representing an item in a shopping list."""
    id: int
    shopping_list_id: int
    ingredient_id: int
    quantity: float
    unit_id: int
    is_purchased: bool
