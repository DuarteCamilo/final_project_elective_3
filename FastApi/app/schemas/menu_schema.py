from pydantic import BaseModel

class Menu(BaseModel):
    """Model representing a menu."""
    id: int
    name: str
    user_id: int
    start_date: str
    end_date: str
