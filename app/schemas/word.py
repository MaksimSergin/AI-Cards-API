from pydantic import BaseModel, Field

class WordRequest(BaseModel):
    """
    Request model for translating a word.

    Attributes:
        user_id (int): The ID of the user requesting the translation.
        word (str): The word that needs to be translated.
    """
    user_id: int = Field(..., gt=0, description="User ID, must be a positive integer")
    word: str = Field(..., min_length=1, description="The word to be translated, cannot be empty")


class WordCreate(BaseModel):
    """
    Model for adding a new word with its translation for a user.

    Attributes:
        word (str): The word being added.
        lang (str): The language of the word (e.g., 'en', 'ru').
        translation (str): The translation of the word.
    """
    word: str = Field(..., min_length=1, description="The word to add, cannot be empty")
    lang: str = Field(..., min_length=2, max_length=25, description="Language code, e.g., 'en' or 'ru'")
    translation: str = Field(..., min_length=1, description="The translation of the word, cannot be empty")
