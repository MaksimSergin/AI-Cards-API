from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class UserWord(Base):
    """
    Association table for many-to-many relationship between users and words.

    Attributes:
        user_id (int): Foreign key referencing User.id.
        word_id (int): Foreign key referencing Word.id.
    """
    __tablename__ = 'user_words'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), primary_key=True)
