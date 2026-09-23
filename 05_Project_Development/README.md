# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Concept explanation
- 3-question MCQ quiz generation
- Passage summarization
- Personalized learning paths

## Architecture

```text
Browser
   |
   v
FastAPI + Jinja2
   |
   +--> /qa --------------------> Gemini
   +--> /explain ---------------> optional LaMini local model
   |                              or Gemini fallback
   +--> /quiz ------------------> Gemini structured JSON
   +--> /summarize -------------> Gemini
   +--> /learn/recommendations -> Gemini
```

The original documentation names Gemini 1.5 Pro and LaMini-Flan-T5-783M. This implementation keeps the same functional architecture but uses the current Google GenAI Python SDK and a configurable Gemini model. The default is `gemini-2.5-flash`, which supports structured output.

## 1. Prerequisites

- Python 3.10+
- VS Code
- A Gemini API key

## 2. Create the environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_real_key
```

Never commit `.env`.

## 4. Run

```bash
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## 5. Optional local LaMini explanation model

The project documentation specifies LaMini-Flan-T5-783M for explanations. To enable it:

```bash
pip install -r requirements-local.txt
```

Then set:

```env
USE_LOCAL_EXPLAINER=true
```

The first explanation request downloads the model from Hugging Face. CPU inference can be slow and memory intensive, so the default is `false`. If the local model fails to load, EduGenie automatically falls back to Gemini.

## 6. API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"Which is the largest ocean?\"}"
```

### Explanation

```bash
curl -X POST http://127.0.0.1:8000/explain ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"Pythagoras theorem\",\"level\":\"beginner\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"The water cycle includes evaporation, condensation and precipitation.\"}"
```

### Summary

```bash
curl -X POST http://127.0.0.1:8000/summarize ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Photosynthesis is the process by which plants use light energy to convert carbon dioxide and water into glucose and oxygen.\"}"
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"SQL\",\"level\":\"beginner\"}"
```

## 7. Test

With the virtual environment active:

```bash
pytest -q
```

The tests mock Gemini, so they do not require a paid API call.

## 8. VS Code

1. Open the `EduGenie` folder.
2. Install the Python extension.
3. Select the `.venv` interpreter.
4. Copy `.env.example` to `.env`.
5. Add the Gemini API key.
6. Open the integrated terminal.
7. Activate the environment.
8. Run `uvicorn main:app --reload`.
9. Open `http://127.0.0.1:8000`.

## 9. Production notes

For deployment, add authentication, rate limiting, logging, secret management, request-size limits, HTTPS, and persistent user/progress storage. The current application intentionally stays lightweight, matching the supplied documentation.
