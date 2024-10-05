from pydantic import BaseModel

class Group(BaseModel):
    """Model representing a user group."""
    id: int
    name: str
