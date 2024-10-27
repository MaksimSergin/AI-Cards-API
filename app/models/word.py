from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Word(Base):
    """
    Word model representing words and their translations.

    Attributes:
        id (int): Unique identifier for each word.
        word (str): The word text.
        lang (str): Language of the word (e.g., 'en', 'ru').
        translate (str): The translation of the word.
        users (relationship): Many-to-many relationship with the User model.
    """
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), nullable=False)
    lang = Column(String(10), nullable=False)
    translate = Column(String(255), nullable=False)

    users = relationship("User", secondary="user_words", back_populates="words")
