"""必输21点游戏引擎。"""


def new_game():
    """创建一局抢21。"""
    return {
        "total": 0,
        "phase": "choose_start",
        "finished": False,
        "winner": None,
        "history": [],
    }


def apply_action(state, action, value=None):
    """执行一次报数操作，返回 (新状态, 响应)。"""
    if state["finished"]:
        return state, {"valid": False, "message": "本局已经结束，请重新开局。", "events": [], "finished": True}
    if action != "move":
        return state, {"valid": False, "message": "未知操作。", "events": [], "finished": False}
    try:
        move = int(value)
    except (TypeError, ValueError):
        return state, {"valid": False, "message": "请输入 1 或 2。", "events": [], "finished": False}
    if move not in (1, 2):
        return state, {"valid": False, "message": "只能加 1 或 2。", "events": [], "finished": False}

    new_state = dict(state)
    new_state["history"] = list(state["history"])
    if new_state["phase"] == "choose_start":
        new_state["total"] = 3
        new_state["history"].append({"player": move, "computer": 3 - move})
        new_state["phase"] = "player_move"
        return new_state, {
            "valid": True,
            "message": f"你报出 {move}，独孤木补到 3。",
            "events": [f"你报出 {move}", "独孤木补到 3"],
            "finished": False,
        }

    player_total = new_state["total"] + move
    if player_total > 21:
        return state, {"valid": False, "message": "加过头了，请重新选择。", "events": [], "finished": False}
    new_state["total"] = player_total
    events = [f"你加到 {player_total}"]
    if player_total == 21:
        new_state["finished"] = True
        new_state["winner"] = "player"
        events.append("你抢先到 21，赢了！")
        return new_state, {"valid": True, "message": "你抢先到 21，赢了！", "events": events, "finished": True}

    computer_move = 3 - move
    new_state["total"] += computer_move
    new_state["history"].append({"player": move, "computer": computer_move})
    events.append(f"独孤木加到 {new_state['total']}")
    if new_state["total"] == 21:
        new_state["finished"] = True
        new_state["winner"] = "computer"
        events.append("独孤木抢先到 21，你输了。")
        return new_state, {"valid": True, "message": "独孤木抢先到 21，你输了。", "events": events, "finished": True}
    return new_state, {
        "valid": True,
        "message": f"你加到 {player_total}，独孤木加到 {new_state['total']}。",
        "events": events,
        "finished": False,
    }
