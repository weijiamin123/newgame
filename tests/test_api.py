from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_new_session_returns_initial_state():
    r = client.post("/api/games/grab21/new")
    assert r.status_code == 200
    data = r.json()
    assert data["session_id"]
    assert data["state"]["total"] == 0


def test_action_updates_session_state():
    r = client.post("/api/games/grab21/new")
    sid = r.json()["session_id"]
    r = client.post("/api/games/grab21/action", json={"session_id": sid, "action": "move", "value": "1"})
    assert r.status_code == 200
    assert r.json()["state"]["total"] == 3


def test_invalid_action_returns_400():
    r = client.post("/api/games/grab21/new")
    sid = r.json()["session_id"]
    r = client.post("/api/games/grab21/action", json={"session_id": sid, "action": "move", "value": "9"})
    assert r.status_code == 400
    assert "只能加 1 或 2" in r.json()["detail"]


def test_unknown_game_returns_404():
    r = client.post("/api/games/missing/new")
    assert r.status_code == 404


def test_missing_session_returns_410():
    r = client.post("/api/games/grab21/action", json={"session_id": "nope", "action": "move", "value": "1"})
    assert r.status_code == 410


def test_state_endpoint_hides_secret():
    r = client.post("/api/games/codebreaker/new")
    sid = r.json()["session_id"]
    r = client.get(f"/api/games/codebreaker/state?session_id={sid}")
    assert r.status_code == 200
    assert "secret" not in r.json()["state"]


def test_index_page_is_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "勇者集结" in r.text
