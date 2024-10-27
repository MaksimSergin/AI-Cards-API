# tests/test_translation.py
import pytest
from unittest.mock import patch
from app.models import User

@pytest.mark.asyncio
@patch('app.services.translation_service.get_translation_from_gpt')
async def test_translate_word(mock_translation, client, async_session_maker):
    """Tests word translation through the API."""
    mock_translation.return_value = "Привет"

    async with async_session_maker() as session:
        user = User(id=1, username="testuser", telegram_id="12345", preferred_lang="russian")
        session.add(user)
        await session.commit()

    payload = {"user_id": 1, "word": "hello"}
    response = await client.post("/translations/explain/", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["word"] == "hello"
    assert "translation" in response_data
    assert response_data["translation"] != ""
