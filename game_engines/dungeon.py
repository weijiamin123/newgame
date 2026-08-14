"""地下城勇士游戏引擎。"""
import copy
import random


def roll_dice():
    """掷三次骰子，返回 3-18 的点数和。"""
    return sum(random.randint(1, 6) for _ in range(3))


def _new_monster():
    return {"hp": 60, "attack": 20, "defense": 10}


def new_game():
    """创建一局地下城。"""
    return {
        "phase": "lobby",
        "player": {"hp": 100, "mp": 100, "attack": 35},
        "floor": 0,
        "monster": None,
        "finished": False,
    }


def _monster_attack(state, events):
    dice = roll_dice()
    if dice > 8:
        damage = state["monster"]["attack"] * (1 + (1 + dice / 21) / 100)
        state["player"]["hp"] -= damage
        events.append(f"怪物攻击成功！你受到 {damage:.2f} 点伤害")
    else:
        events.append("怪物攻击落空")


def _resolve_player_action(state, events):
    if state["monster"]["hp"] <= 0:
        state["floor"] += 1
        state["monster"] = None
        state["phase"] = "camp"
        events.append(f"怪物倒下了！你通关第 {state['floor']} 层。")
        return
    _monster_attack(state, events)
    if state["player"]["hp"] <= 0:
        state["phase"] = "lobby"
        state["monster"] = None
        events.append("你死了！回到地城入口。")


def apply_action(state, action, value=None):
    """执行一次地下城操作，返回 (新状态, 响应)。"""
    new_state = copy.deepcopy(state)
    events = []

    if new_state["phase"] == "lobby":
        if action == "start":
            new_state["player"] = {"hp": 100, "mp": 100, "attack": 35}
            new_state["floor"] = 1
            new_state["monster"] = _new_monster()
            new_state["player"]["mp"] += 1
            new_state["phase"] = "battle"
            message = "你在地下城门口醒来，里面传出嘶嘶叫声。第 1 层出现一只怪物。"
            return new_state, {"valid": True, "message": message, "events": [message], "finished": False}
        if action == "quit":
            new_state["finished"] = True
            return new_state, {"valid": True, "message": "已退出地下城。", "events": ["已退出地下城"], "finished": True}
        return new_state, {"valid": False, "message": "请先开始游戏。", "events": [], "finished": False}

    if new_state["phase"] == "camp":
        if action == "next_floor":
            new_state["floor"] += 1
            new_state["monster"] = _new_monster()
            new_state["player"]["mp"] += 1
            new_state["phase"] = "battle"
            message = f"你进入第 {new_state['floor']} 层，怪物出现。"
            return new_state, {"valid": True, "message": message, "events": [message], "finished": False}
        if action == "quit":
            new_state["phase"] = "lobby"
            new_state["monster"] = None
            return new_state, {"valid": True, "message": "你逃回了地城入口。", "events": ["你逃回了地城入口"], "finished": False}
        return new_state, {"valid": False, "message": "请选择进入下一层或返回。", "events": [], "finished": False}

    if new_state["phase"] == "battle":
        if action == "attack":
            dice = roll_dice()
            if dice >= 3:
                damage = new_state["player"]["attack"] * (1 + dice / 100)
                new_state["monster"]["hp"] -= damage
                events.append(f"点数为 {dice}，攻击成功，造成 {damage:.2f} 点伤害")
            else:
                events.append(f"点数为 {dice}，判定无效，攻击失败")
            _resolve_player_action(new_state, events)
        elif action == "skill":
            if new_state["player"]["mp"] < 10:
                return new_state, {"valid": False, "message": "你的 MP 不足，无法施放技能！", "events": [], "finished": False}
            dice = roll_dice()
            if dice >= 12:
                new_state["monster"]["hp"] -= 40
                new_state["player"]["hp"] += 40
                new_state["player"]["mp"] -= 10
                events.append(f"点数为 {dice}，技能成功！造成 40 伤害，回复 40 HP")
            else:
                events.append(f"点数为 {dice}，判定无效，技能失败")
            _resolve_player_action(new_state, events)
        elif action == "run":
            dice = roll_dice()
            if dice >= 9:
                new_state["phase"] = "camp"
                new_state["monster"] = None
                events.append(f"点数为 {dice}，你成功逃跑了！")
            else:
                events.append(f"点数为 {dice}，逃跑失败！")
                _monster_attack(new_state, events)
                if new_state["player"]["hp"] <= 0:
                    new_state["phase"] = "lobby"
                    new_state["monster"] = None
                    events.append("你死了！回到地城入口。")
        elif action == "quit":
            new_state["phase"] = "lobby"
            new_state["monster"] = None
            events.append("你离开了地下城。")
        else:
            return new_state, {"valid": False, "message": "未知操作。", "events": [], "finished": False}
        return new_state, {"valid": True, "message": "\n".join(events), "events": events, "finished": new_state["finished"]}

    return new_state, {"valid": False, "message": "未知状态。", "events": [], "finished": False}
