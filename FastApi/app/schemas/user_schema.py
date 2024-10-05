from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """Model representing a user."""
    id: int
    username: str
    email: str
    password_hash: str
    profile_picture: Optional[str] = None
