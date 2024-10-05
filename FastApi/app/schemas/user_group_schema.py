from pydantic import BaseModel

class UserGroup(BaseModel):
    """Model representing a relationship between user and group."""
    user_id: int
    group_id: int
