# tests/test_user_words.py
import pytest
from app.models import User, Word, UserWord

@pytest.mark.asyncio
async def test_get_user_words(client, async_session_maker):
    """Tests fetching all words associated with a user via the API."""

    async with async_session_maker() as session:
        user = User(id=1, username="testuser", telegram_id="12345", preferred_lang="russian")
        session.add(user)
        await session.commit()

        word = Word(id=1, word="hello", lang="en", translate="Привет")
        session.add(word)
        await session.commit()

        user_word = UserWord(user_id=1, word_id=1)
        session.add(user_word)
        await session.commit()

    response = await client.get("/users/1/words/")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_id"] == 1
    assert len(response_data["words"]) == 1
    assert response_data["words"][0]["word"] == "hello"
    assert response_data["words"][0]["translation"] == "Привет"
