from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""
Create a personalized learning path for the topic "{topic}".

Learner level: {level}

Organize it from foundational concepts toward advanced concepts. Include:
- stages in a sensible order
- suggested time for each stage
- what the learner should be able to do after each stage
- practical exercises/projects
- trustworthy resource types (official docs, books, courses, videos)
- a simple way to check mastery

Keep the plan realistic and educational. Do not fabricate exact URLs.
"""
    return generate_text(prompt)
