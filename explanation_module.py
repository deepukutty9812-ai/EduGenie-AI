from __future__ import annotations

from config import settings
from gemini_client import generate_text

_local_pipeline = None


def _get_local_pipeline():
    global _local_pipeline
    if _local_pipeline is None:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Local explanation requires transformers and torch. "
                "Either install the optional local dependencies or set USE_LOCAL_EXPLAINER=false."
            ) from exc

        _local_pipeline = pipeline(
            "text2text-generation",
            model=settings.local_explainer_model,
            device=-1,
        )
    return _local_pipeline


def _local_explanation(topic: str, level: str) -> str:
    generator = _get_local_pipeline()
    prompt = (
        f"Explain {topic} to a {level} learner. "
        "Use simple language, a short example, and avoid unnecessary detail."
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(topic: str, level: str = "beginner") -> str:
    if settings.use_local_explainer:
        try:
            return _local_explanation(topic, level)
        except Exception:
            # Keep the application usable if the optional local model cannot load.
            pass

    prompt = f"""
Explain "{topic}" to a {level} learner.

Structure the answer as:
- Simple definition
- How it works
- One intuitive example
- Common mistake to avoid
- One quick check question

Use plain language and keep it concise.
"""
    return generate_text(prompt)
