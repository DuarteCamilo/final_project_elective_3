from pydantic import BaseModel, Field, validator

class Recipe(BaseModel):
    """Model representing a recipe."""
    id: int
    name: str
    description: str 
    instructions: str 
    preparation_time: int = Field(..., gt=0)
    datosNutricionales: str
    type: str 
    difficulty: str
    is_public: bool
    user_id: int

    # pylint: disable=E0213
    @validator("preparation_time")
    def valid_preparation_time(cls, v):
        """Ensure preparation time is positive."""
        if v <= 0:
            raise ValueError("Preparation time must be positive")
        return v
