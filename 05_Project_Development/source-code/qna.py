from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
Answer the student's question below.

Question:
{question}

Requirements:
- Give a direct answer first.
- Explain the reasoning or important context briefly.
- Use plain language suitable for a learner.
- If the question is ambiguous, state the ambiguity rather than inventing facts.
"""
    return generate_text(prompt)
