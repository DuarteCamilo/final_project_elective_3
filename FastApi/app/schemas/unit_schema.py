from pydantic import BaseModel

class Unit(BaseModel):
    """Model representing a unit."""
    id: int
    name: str
