import time
from typing import Optional
from app.config.config import OPENAI_API_KEY
from openai import OpenAI

if not OPENAI_API_KEY:
    raise EnvironmentError("API key for OpenAI is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_translation_from_gpt(word: str, target_language: str = "russian") -> Optional[str]:
    """
    Fetches a brief translation of the given word from GPT in the specified target language.

    Args:
        word (str): The word to translate.
        target_language (str): The language to translate the word into.

    Returns:
        Optional[str]: The translated word, or None if no valid response is received.

    Raises:
        Exception: If the response from OpenAI is invalid or the request fails.
    """
    try:

        language_instruction = f"Explain this word in {target_language} in a few words: {word}"

        messages = [
            {
                "role": "user",
                "content": language_instruction
            }
        ]

        start_time = time.time()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        print(f"Translation request took {time.time() - start_time:.2f} seconds")

        if response and response.choices:
            return response.choices[0].message.content

        return None

    except Exception as e:
        print(f"Error while getting translation from OpenAI: {e}")
        raise Exception(f"Error while getting translation from OpenAI: {e}")
