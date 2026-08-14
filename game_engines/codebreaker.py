"""绝密2025游戏引擎。"""
import random


def new_game():
    """创建一局密码破译。"""
    return {
        "secret": random.sample(range(1, 10), 4),
        "attempts_left": 8,
        "guesses": [],
        "finished": False,
        "won": False,
    }


def public_state(state):
    """返回不含密码的公开状态。"""
    public = dict(state)
    public.pop("secret", None)
    return public


def apply_action(state, action, value=None):
    """提交一次猜测，返回 (新状态, 响应)。"""
    if state["finished"]:
        return state, {"valid": False, "message": "本局已经结束，请重新开局。", "events": [], "finished": True}
    if action != "guess":
        return state, {"valid": False, "message": "未知操作。", "events": [], "finished": False}
    guess = str(value or "").strip()
    if len(guess) != 4 or not guess.isdigit() or "0" in guess or len(set(guess)) != 4:
        return state, {"valid": False, "message": "请输入 4 位不重复的数字（1-9）。", "events": [], "finished": False}

    new_state = dict(state)
    new_state["guesses"] = list(state["guesses"])
    secret = new_state["secret"]
    digits = [int(ch) for ch in guess]
    a = sum(1 for i, d in enumerate(digits) if d == secret[i])
    b = sum(1 for d in digits if d in secret) - a
    feedback = f"{a}A{b}B"
    new_state["attempts_left"] -= 1
    new_state["guesses"].append({"guess": guess, "feedback": feedback})
    if a == 4:
        new_state["finished"] = True
        new_state["won"] = True
        message = "你赢了，游戏结束！密码就是 " + guess + "。"
    elif new_state["attempts_left"] <= 0:
        new_state["finished"] = True
        new_state["won"] = False
        message = "8 次机会用完了，正确密码是 " + "".join(str(d) for d in secret) + "。"
    else:
        message = f"反馈：{feedback}，还剩 {new_state['attempts_left']} 次机会。"
    return new_state, {"valid": True, "message": message, "events": [message], "finished": new_state["finished"]}
