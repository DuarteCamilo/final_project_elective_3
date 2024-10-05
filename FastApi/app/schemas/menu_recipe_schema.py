from pydantic import BaseModel

class MenuRecipe(BaseModel):
    """Model representing a recipe in a menu."""
    menu_id: int
    recipe_id: int
    meal_time: str
    planned_date: str
