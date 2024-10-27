import pytest
from unittest.mock import patch
from app import create_app
from app.models import User
from sqlalchemy import text


app = create_app()

@pytest.mark.asyncio
@patch('app.services.translation_service.get_translation_from_gpt')
async def test_add_word(mock_translation, client, async_session_maker):
    """Tests adding a new word for a user via the API."""
    mock_translation.return_value = "Привет"

    async with async_session_maker() as session:
        user = User(id=1, username="testuser", telegram_id="12345", preferred_lang="russian")
        session.add(user)
        await session.commit()

    payload = {"word": "helloooooo", "lang": "en", "translation": "Привет"}
    response = await client.post("/users/1/words/add", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Word added successfully"
    assert response_data["word"] == "helloooooo"
    assert response_data["translation"] == "Привет"

    async with async_session_maker() as session:
        result = await session.execute(text("SELECT * FROM words WHERE word = 'helloooooo'"))
        word = result.fetchone()
        assert word is not None
