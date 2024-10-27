from pydantic import BaseModel, Field
from typing import Optional, List


class UserBase(BaseModel):
    """
    Base schema for User, used as a base for other User schemas.

    Attributes:
        username (Optional[str]): The username of the user.
        preferred_lang (Optional[str]): The user's preferred language code.
    """
    username: Optional[str] = Field(None, max_length=50, description="Username of the user")
    preferred_lang: Optional[str] = Field(None, max_length=10, description="Preferred language of the user")


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        telegram_id (str): The Telegram ID for the user, required at creation.
    """
    telegram_id: str = Field(..., max_length=100, description="Telegram ID of the user")


class UserResponse(UserBase):
    """
    Schema for returning user data in responses.

    Attributes:
        id (int): The ID of the user.
    """
    id: int = Field(..., description="Unique ID of the user")

    class Config:
        orm_mode = True


class UserWithWords(UserResponse):
    """
    Schema for returning user data along with their associated words.

    Attributes:
        words (List[dict]): A list of words associated with the user.
    """
    words: List[dict] = Field([], description="List of words associated with the user")
