from pydantic import BaseModel

class Notification(BaseModel):
    """Model representing a notification."""
    id: int
    user_id: int
    message: str
    created_at: str  
    is_read: bool
