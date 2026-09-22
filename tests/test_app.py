from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation():
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422


def test_qa(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda question: "The answer.")
    response = client.post("/qa", json={"question": "What is photosynthesis?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "The answer."


def test_explain(monkeypatch):
    monkeypatch.setattr(main, "explain_concept", lambda topic, level: "Simple explanation.")
    response = client.post(
        "/explain",
        json={"topic": "gravity", "level": "beginner"},
    )
    assert response.status_code == 200
    assert response.json()["explanation"] == "Simple explanation."


def test_summary(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Short summary.")
    response = client.post("/summarize", json={"text": "Long text."})
    assert response.status_code == 200
    assert response.json()["summary"] == "Short summary."


def test_learning_path(monkeypatch):
    monkeypatch.setattr(
        main,
        "get_learning_recommendations",
        lambda topic, level: "Stage 1 -> Stage 2",
    )
    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "beginner"},
    )
    assert response.status_code == 200
    assert response.json()["learning_path"] == "Stage 1 -> Stage 2"
