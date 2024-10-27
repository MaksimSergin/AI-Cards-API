from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.word import WordRequest
from app.models.user import User
from app.services.translation_service import get_translation_from_gpt
from app.config.config import get_db

router = APIRouter()

@router.post("/explain/")
async def translate(request: WordRequest, db: AsyncSession = Depends(get_db)):
    """
    Translates the given word, considering the user's preferred language.

    Args:
        request (WordRequest): The request containing user_id and word to be translated.
        db (AsyncSession): Database session provided by dependency injection.

    Returns:
        dict: A dictionary with the original word and its translation.

    Raises:
        HTTPException: If the user is not found or translation fails.
    """

    user_query = await db.execute(select(User).where(User.id == request.user_id))
    user = user_query.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    target_language = user.preferred_lang if user.preferred_lang else "english"

    try:
        translation = get_translation_from_gpt(request.word, target_language=target_language)
        if not translation:
            raise HTTPException(status_code=400, detail="Unable to translate the word.")
        return {"word": request.word, "translation": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
