from pydantic import BaseModel

class FavoriteRecipe(BaseModel):
    """Model representing a user's favorite recipe."""
    id: int
    user_id: int
    recipe_id: int
