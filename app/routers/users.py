from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.word import WordCreate
from app.models import User, Word, UserWord
from app.config.config import get_db

router = APIRouter()

@router.get("/{user_id}/words/")
async def get_user_words(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all words added by a specific user.

    Args:
        user_id (int): ID of the user.
        db (AsyncSession): Database session provided by dependency injection.

    Returns:
        dict: A dictionary containing the user's words and translations.

    Raises:
        HTTPException: If the user or words cannot be found.
    """

    user_query = await db.execute(select(User).where(User.id == user_id))
    user = user_query.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    word_query = await db.execute(
        select(Word).join(UserWord).where(UserWord.user_id == user_id)
    )
    words = word_query.scalars().all()

    if not words:
        raise HTTPException(status_code=404, detail="No words found for this user")

    return {
        "user_id": user_id,
        "words": [{"word": word.word, "translation": word.translate} for word in words]
    }

@router.post("/{user_id}/words/add")
async def add_word(user_id: int, request: WordCreate, db: AsyncSession = Depends(get_db)):
    """
    Adds a new word for a specific user.

    Args:
        user_id (int): ID of the user.
        request (WordCreate): The word creation request containing word, language, and translation.
        db (AsyncSession): Database session provided by dependency injection.

    Returns:
        dict: A message indicating successful addition of the word.

    Raises:
        HTTPException: If the user does not exist or there is an error in adding the word.
    """

    user_query = await db.execute(select(User).where(User.id == user_id))
    user = user_query.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_word = Word(word=request.word, lang=request.lang, translate=request.translation)
    db.add(new_word)
    await db.commit()

    db.add(UserWord(user_id=user_id, word_id=new_word.id))
    await db.commit()

    return {"message": "Word added successfully", "word": new_word.word, "translation": new_word.translate}
