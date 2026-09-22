from config import settings
from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text[: settings.max_input_chars]
    prompt = f"""
Summarize the following educational passage for quick revision.

Passage:
{text}

Return:
1. A short summary in 1-2 paragraphs.
2. A "Key points" bullet list with the most important ideas.

Do not add facts that are not supported by the passage.
"""
    return generate_text(prompt)
