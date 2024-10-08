from pydantic import BaseModel

class UserGroup(BaseModel):
    """Model representing a relationship between user and group."""
    id : int
    user_id: int
    group_id: int
