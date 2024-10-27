from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    """
    User model representing users in the system.

    Attributes:
        id (int): Unique identifier for each user.
        username (str): Optional username, unique per user.
        telegram_id (str): Optional unique identifier associated with the user's Telegram.
        preferred_lang (str): The preferred language of the user.
        words (relationship): Many-to-many relationship with the Word model.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    telegram_id = Column(String(100), unique=True, nullable=True)
    preferred_lang = Column(String(10), nullable=True)

    words = relationship("Word", secondary="user_words", back_populates="users")
