import time
from functools import lru_cache

from google import genai

from config import settings


class GeminiQuotaError(Exception):
    """Raised when the Gemini project quota has been exhausted."""


class GeminiTemporaryError(Exception):
    """Raised when Gemini is temporarily unavailable."""


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def _is_daily_quota_error(error_text: str) -> bool:
    text = error_text.lower()

    return (
        "generat_content_free_tier_requests" in text
        or "generate_content_free_tier_requests" in text
        or "generaterequestsperdayperproject" in text
        or "generate_requests_per_day" in text
        or "quota exceeded" in text
        or "daily quota" in text
    )


def _is_temporary_error(error_text: str) -> bool:
    text = error_text.lower()

    return (
        "503" in text
        or "unavailable" in text
        or "high demand" in text
        or "temporarily" in text
    )


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
) -> str:

    client = get_client()

    config = {
        "system_instruction": (
            system_instruction
            if system_instruction
            else (
                "You are EduGenie, a careful educational assistant. "
                "Be accurate, concise, and clear."
            )
        ),
        "temperature": 0.4,
    }

    # Only retry temporary service-capacity errors.
    # Do NOT repeatedly retry a daily quota exhaustion.
    max_attempts = 4
    delays = [3, 8, 15]

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        except Exception as exc:
            error_text = str(exc)

            # Daily quota exhausted.
            if _is_daily_quota_error(error_text):
                raise GeminiQuotaError(
                    "Gemini API daily quota has been reached. "
                    "Please wait until the quota resets or enable a "
                    "higher Gemini API usage tier."
                ) from exc

            # Temporary Gemini service problem.
            if _is_temporary_error(error_text):
                if attempt < max_attempts - 1:
                    time.sleep(delays[attempt])
                    continue

                raise GeminiTemporaryError(
                    "Gemini is temporarily unavailable. "
                    "Please try again in a few moments."
                ) from exc

            # Any other error should be returned immediately.
            raise

    raise GeminiTemporaryError(
        "Gemini is temporarily unavailable. Please try again later."
    )