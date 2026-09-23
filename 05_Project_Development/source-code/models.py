from typing import Literal

from pydantic import BaseModel, Field, field_validator


Level = Literal["beginner", "intermediate", "advanced"]


class QARequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)

    @field_validator("question")
    @classmethod
    def clean_question(cls, value: str) -> str:
        return value.strip()


class TextRequest(BaseModel):
    text: str = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return value.strip()


class ExplanationRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=4000)
    level: Level = "beginner"


class QuizRequest(TextRequest):
    pass


class SummaryRequest(TextRequest):
    pass


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=4000)
    level: Level = "beginner"


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


class ErrorResponse(BaseModel):
    detail: str