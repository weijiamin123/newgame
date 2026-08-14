"""FastAPI 入口：提供游戏 API 并托管静态前端。"""
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from game_engines import codebreaker, dungeon, grab21, history

GAMES = {
    "history": history,
    "grab21": grab21,
    "codebreaker": codebreaker,
    "dungeon": dungeon,
}

SESSIONS = {}

app = FastAPI(title="沃林小游戏 API")


class ActionRequest(BaseModel):
    session_id: str
    action: str
    value: str | None = None


def _public_state(game: str, state: dict) -> dict:
    if game == "codebreaker":
        return codebreaker.public_state(state)
    return state


@app.post("/api/games/{game}/new")
def create_game(game: str):
    engine = GAMES.get(game)
    if engine is None:
        raise HTTPException(status_code=404, detail="未知游戏")
    session_id = uuid.uuid4().hex
    state = engine.new_game()
    SESSIONS[session_id] = state
    return {"session_id": session_id, "state": _public_state(game, state)}


@app.post("/api/games/{game}/action")
def take_action(game: str, request: ActionRequest):
    engine = GAMES.get(game)
    if engine is None:
        raise HTTPException(status_code=404, detail="未知游戏")
    state = SESSIONS.get(request.session_id)
    if state is None:
        raise HTTPException(status_code=410, detail="会话已失效，请重新开局")
    new_state, response = engine.apply_action(state, request.action, request.value)
    if not response["valid"]:
        raise HTTPException(status_code=400, detail=response["message"])
    SESSIONS[request.session_id] = new_state
    return {"state": _public_state(game, new_state), "response": response}


@app.get("/api/games/{game}/state")
def read_state(game: str, session_id: str):
    engine = GAMES.get(game)
    if engine is None:
        raise HTTPException(status_code=404, detail="未知游戏")
    state = SESSIONS.get(session_id)
    if state is None:
        raise HTTPException(status_code=410, detail="会话已失效，请重新开局")
    return {"state": _public_state(game, state)}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
