from __future__ import annotations
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    ErrorResponse,
    ExplanationRequest,
    LearningPathRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
)
from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from learning_path import get_learning_recommendations
from gemini_client import GeminiQuotaError, GeminiTemporaryError

app = FastAPI(
    title="EduGenie",
    description="Gemini-powered educational learning assistant.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
def handle_gemini_error(exc: Exception) -> HTTPException:
    if isinstance(exc, GeminiQuotaError):
        return HTTPException(
            status_code=429,
            detail=(
                "Gemini API quota has been reached. "
                "Please wait for the quota to reset or enable "
                "a higher Gemini API usage tier."
            ),
        )

    if isinstance(exc, GeminiTemporaryError):
        return HTTPException(
            status_code=503,
            detail=(
                "Gemini is temporarily busy. "
                "Please try again in a few moments."
            ),
        )

    return HTTPException(
        status_code=502,
        detail=f"{type(exc).__name__}: {exc}",
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "local_explainer_enabled": settings.use_local_explainer,
    }


@app.post("/qa")
async def qa(payload: QARequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: ExplanationRequest):
    try:
        return {"explanation": explain_concept(payload.topic, payload.level)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return generate_quiz(payload.text)
    except Exception as exc:
        raise handle_gemini_error(exc) from exc


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    try:
        return {"summary": summarize_text(payload.text)}
    except Exception as exc:
        raise handle_gemini_error(exc) from exc


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    try:
        return {"learning_path": get_learning_recommendations(payload.topic, payload.level)}
    except Exception as exc:
        raise handle_gemini_error(exc) from exc
