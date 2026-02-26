from google import genai
from google.genai import types

from .config import GEMINI_API_KEY, GEMINI_MODEL
from .models import BuddyResponse
from .prompts import SYSTEM_PROMPT


def create_client() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def query(scene_description: str, client: genai.Client) -> BuddyResponse:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=scene_description,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=BuddyResponse,
            temperature=0.7,
        ),
    )
    return BuddyResponse.model_validate_json(response.text)
