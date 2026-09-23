from __future__ import annotations

from google.genai import types
from pydantic import ValidationError

from config import settings
from gemini_client import get_client
from models import QuizResponse


def generate_quiz(text: str) -> dict:
    text = text[: settings.max_input_chars]
    client = get_client()

    prompt = f"""
Create exactly 3 multiple-choice questions from the passage below.

Passage:
{text}

Rules:
- Each question must have exactly 4 distinct options.
- Exactly one option must be correct.
- The correct_answer must exactly match one option.
- Include a short explanation for why the answer is correct.
- Questions must test understanding, not obscure wording.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=QuizResponse,
        ),
    )

    raw = getattr(response, "text", None)
    if not raw:
        raise RuntimeError("Gemini returned an empty quiz response.")

    try:
        quiz = QuizResponse.model_validate_json(raw)
    except ValidationError as exc:
        raise RuntimeError(f"Quiz validation failed: {exc}") from exc

    for item in quiz.questions:
        if item.correct_answer not in item.options:
            raise RuntimeError(
                "Gemini returned a quiz where the correct answer is not one of the options."
            )

    return quiz.model_dump()
