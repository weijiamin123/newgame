# 游戏合集 FastAPI 前端实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为现有四款控制台小游戏新增 FastAPI 后端和浏览器单页前端，让它们可以在网页上完整游玩，同时保留 `new_game.py` 命令行版本。

**Architecture:** FastAPI 提供 JSON API 并托管 `static/` 前端；四款游戏规则抽成 `game_engines/` 下的纯 Python 状态机；前端单页应用通过 `fetch` 调用 API，按 `session_id` 维护每局状态。

**Tech Stack:** Python 3.10+、FastAPI、Uvicorn、pytest、httpx（TestClient）、原生 HTML/CSS/JavaScript。

**环境说明：** 当前环境为 Python 3.14.6，尚未安装 `fastapi`、`uvicorn`、`pytest`、`httpx`，Task 0 会安装。

## 文件结构

- `app.py`：FastAPI 入口，注册 `/api/games/<game>` 路由并挂载静态目录。
- `game_engines/__init__.py`：引擎包标记。
- `game_engines/history.py`：野史冲浪引擎。
- `game_engines/grab21.py`：必输21点引擎。
- `game_engines/codebreaker.py`：绝密2025引擎。
- `game_engines/dungeon.py`：地下城勇士引擎。
- `static/index.html`：单页应用骨架（大厅 + 通用游戏视图）。
- `static/style.css`：深夜地下城主题样式。
- `static/app.js`：API 客户端和四个游戏的界面渲染。
- `tests/test_history.py`、`tests/test_grab21.py`、`tests/test_codebreaker.py`、`tests/test_dungeon.py`、`tests/test_api.py`：引擎和 API 测试。
- `requirements.txt`：运行时和测试依赖。
- `.gitignore`：忽略缓存和本地文件。
- `AGENTS.md`：末尾任务中同步更新项目指南。

每个引擎统一暴露：

- `new_game() -> state`：创建 JSON 可序列化的初始状态。
- `apply_action(state, action, value) -> (state, response)`：执行操作并返回新状态。
- `response` 固定为 `{"valid": bool, "message": str, "events": list[str], "finished": bool}`。

---

### Task 0: 项目脚手架与依赖

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `game_engines/__init__.py`
- Create: `static/index.html`（占位页，后续任务替换）

- [ ] **Step 1: 创建 requirements.txt**

```text
fastapi
uvicorn
pytest
httpx
```

- [ ] **Step 2: 创建 .gitignore**

```text
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.superpowers/
```

- [ ] **Step 3: 创建包和静态目录占位**

`game_engines/__init__.py` 内容：

```python
"""四款小游戏的纯逻辑引擎包。"""
```

`static/index.html` 占位内容：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>勇者集结</title>
</head>
<body>
  <h1>勇者集结</h1>
  <p>前端建设中</p>
</body>
</html>
```

- [ ] **Step 4: 安装依赖**

Run: `pip install -r requirements.txt`

Expected: 安装成功，无报错。

- [ ] **Step 5: 验证依赖可导入**

Run: `python -c "import fastapi, uvicorn, pytest, httpx; print('ok')"`

Expected: `ok`

- [ ] **Step 6: 初始化 Git 并提交基线**

```bash
git init
git add -A
git commit -m "chore: scaffold fastapi game hub"
```

Expected: 基线提交成功（`.superpowers/` 已被忽略）。

---

### Task 1: 野史冲浪引擎

**Files:**
- Create: `game_engines/history.py`
- Test: `tests/test_history.py`

- [ ] **Step 1: 写失败测试**

```python
from game_engines import history


def test_new_game_has_first_question():
    state = history.new_game()
    assert state["finished"] is False
    assert state["question_index"] == 0
    assert state["score"] == 0
    assert state["current_question"]["options"]


def test_correct_choice_increments_score():
    state = history.new_game()
    question = state["current_question"]
    option = question["correct"][0] + 1
    state, response = history.apply_action(state, "choose", str(option))
    assert response["valid"] is True
    assert state["score"] == 1
    assert "当前得分" in response["message"]


def test_wrong_choice_no_penalty_by_default():
    state = history.new_game()
    question = state["current_question"]
    wrong = next(i for i in range(1, len(question["options"]) + 1) if i - 1 not in question["correct"])
    state, response = history.apply_action(state, "choose", str(wrong))
    assert response["valid"] is True
    assert state["score"] == 0


def test_invalid_choice_returns_valid_false():
    state = history.new_game()
    state, response = history.apply_action(state, "choose", "99")
    assert response["valid"] is False
    assert state["score"] == 0


def test_play_through_all_questions():
    state = history.new_game()
    turns = 0
    while not state["finished"]:
        question = state["current_question"]
        option = question["correct"][0] + 1
        state, response = history.apply_action(state, "choose", str(option))
        turns += 1
        assert response["valid"] is True
    assert turns == state["total"]
    assert state["score"] == state["total"]
    assert "最终得分" in response["message"]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_history.py -q`

Expected: FAIL，`ModuleNotFoundError: No module named 'game_engines.history'`

- [ ] **Step 3: 实现 history.py**

```python
"""野史冲浪游戏引擎。

题目与反馈取自 new_game.py；网页版按符合史实的答案计分，
修正控制台版本中个别题目答错却加分/答对却减分的笔误。
"""

QUESTIONS = [
    {
        "question": "据野史记载，赵姬在认识异人之前已经怀有身孕，吕不韦才是嬴政的生父，这是真的吗？",
        "options": ["是真的", "是假的"],
        "correct": [1],
        "feedback_correct": "尔乃朕之心腹，赐名赵高！",
        "feedback_wrong": "无稽之谈，把你烧成兵马俑下去陪始皇帝。",
        "wrong_penalty": False,
    },
    {
        "question": "秦将白起号称杀神，请问是他灭了赵国吗？",
        "options": ["是真的", "是假的"],
        "correct": [1],
        "feedback_correct": "不错，你的历史小贴士还算可以。",
        "feedback_wrong": "历史上是王翦灭的赵国，白起被秦昭襄王赐死，根本熬不到灭赵的时候。",
        "wrong_penalty": False,
    },
    {
        "question": "民间常有“楚虽三户，亡秦必楚”的说法，请问项羽的父亲是谁？",
        "options": ["项梁", "项伯", "项少龙"],
        "correct": [0, 1],
        "feedback_correct": "史料没有明确记载，壮士如此勇猛，却不知他爸是谁，肯定有内涵，加一分！",
        "feedback_wrong": "少看点穿越剧，史书里并没有项少龙这个人。",
        "wrong_penalty": True,
    },
    {
        "question": "以下哪个战役发生在战国时期？",
        "options": ["巨鹿之战", "垓下之战", "桂陵之战", "暗渡陈仓"],
        "correct": [2],
        "feedback_correct": "恭喜答对！兵家亚圣孙膑复仇庞涓之战，鬼谷门人的纷争一直没有停过。",
        "feedback_wrong": "答案错误，自己去查查吧。",
        "wrong_penalty": False,
    },
    {
        "question": "楚汉争霸中，成语“背水一战”指的是谁？",
        "options": ["项羽", "韩信", "刘邦", "周勃"],
        "correct": [1],
        "feedback_correct": "恭喜答对！韩信号称兵仙，多个成语都出自他，可惜最终兔死狗烹。",
        "feedback_wrong": "答错了，虽然这几位也很厉害。",
        "wrong_penalty": False,
    },
    {
        "question": "“封狼居胥、饮马瀚海”是中国古代武将的最高荣耀，汉朝时期做到这一点的人是谁？",
        "options": ["李广", "卫青", "霍去病", "周亚夫"],
        "correct": [2],
        "feedback_correct": "恭喜答对！霍去病十七岁随卫青出征，封狼居胥、饮马瀚海，可惜英年早逝。",
        "feedback_wrong": "答错了，没有第二次机会给你。",
        "wrong_penalty": False,
    },
    {
        "question": "王莽篡汉建立新朝，之后绿林赤眉起义，请问最终灭亡东汉的是哪个？",
        "options": ["曹操", "曹丕", "司马懿", "司马炎"],
        "correct": [1],
        "feedback_correct": "老子没做的事，儿子做了。曹丕逼汉献帝禅让，东汉正式灭亡。",
        "feedback_wrong": "答错了，东汉的终结者是曹丕。",
        "wrong_penalty": True,
    },
    {
        "question": "蜀汉算汉朝吗？",
        "options": ["算", "不算"],
        "correct": [1],
        "feedback_correct": "确实不算。关羽被吕蒙偷袭之后，蜀汉已经偏离诸葛亮最初的战略部署，三国里基本最弱。",
        "feedback_wrong": "刘备虽是汉室后裔，但蜀汉并没有延续东汉法统。",
        "wrong_penalty": False,
    },
    {
        "question": "“天策上将”指的是谁？",
        "options": ["秦叔宝", "尉迟恭", "李世民", "李靖"],
        "correct": [2],
        "feedback_correct": "恭喜答对！天策上将，封无可封。",
        "feedback_wrong": "答错了。李世民-天策上将，李靖-唐朝初期的战神。",
        "wrong_penalty": False,
    },
    {
        "question": "以下谁没有帮助李世民参与玄武门之变？",
        "options": ["长孙无忌", "魏征", "秦叔宝", "程咬金"],
        "correct": [1],
        "feedback_correct": "恭喜答对！魏征是太子李建成的心腹，玄武门之后才被李世民收服。",
        "feedback_wrong": "答错了，没有第二次机会给你。",
        "wrong_penalty": False,
    },
    {
        "question": "李白、杜甫、高适中，大器晚成的是谁？",
        "options": ["李白", "杜甫", "高适", "白居易"],
        "correct": [2],
        "feedback_correct": "恭喜答对！高适在安史之乱爆发后，52 岁才开始转正。莫愁前路无知己，天下谁人不识君。",
        "feedback_wrong": "打错了。",
        "wrong_penalty": False,
    },
    {
        "question": "中国古代唯一以女儿身称帝的皇帝是谁？",
        "options": ["吕雉", "武则天", "慈禧"],
        "correct": [1],
        "feedback_correct": "恭喜答对！武则天先废了几个儿子，公元 690 年称帝，改国号为周。",
        "feedback_wrong": "答错了，扣一分，回去好好补课。",
        "wrong_penalty": True,
    },
]


def new_game():
    """创建一局野史冲浪。"""
    return {
        "question_index": 0,
        "score": 0,
        "total": len(QUESTIONS),
        "finished": False,
        "current_question": QUESTIONS[0],
        "last_feedback": None,
        "last_correct": None,
    }


def apply_action(state, action, value=None):
    """执行一次答题操作，返回 (新状态, 响应)。"""
    if state["finished"]:
        return state, {"valid": False, "message": "本局已经结束，请重新开局。", "events": [], "finished": True}
    if action != "choose":
        return state, {"valid": False, "message": "未知操作。", "events": [], "finished": False}
    try:
        choice = int(value)
    except (TypeError, ValueError):
        return state, {"valid": False, "message": "请输入选项编号。", "events": [], "finished": False}
    question = state["current_question"]
    if choice < 1 or choice > len(question["options"]):
        return state, {"valid": False, "message": f"请输入 1-{len(question['options'])} 之间的选项。", "events": [], "finished": False}

    new_state = dict(state)
    choice_index = choice - 1
    correct = choice_index in question["correct"]
    if correct:
        new_state["score"] += 1
        feedback = question["feedback_correct"]
    else:
        if question["wrong_penalty"]:
            new_state["score"] -= 1
        feedback = question["feedback_wrong"]

    new_state["last_feedback"] = feedback
    new_state["last_correct"] = correct
    next_index = new_state["question_index"] + 1
    if next_index >= new_state["total"]:
        new_state["finished"] = True
        message = f"{feedback}\n答题结束，最终得分：{new_state['score']} / {new_state['total']}。"
    else:
        new_state["question_index"] = next_index
        new_state["current_question"] = QUESTIONS[next_index]
        message = f"{feedback}\n当前得分：{new_state['score']}。"
    return new_state, {"valid": True, "message": message, "events": [message], "finished": new_state["finished"]}
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_history.py -q`

Expected: `5 passed`

- [ ] **Step 5: 提交**

```bash
git add game_engines/history.py tests/test_history.py
git commit -m "feat: add history quiz engine"
```

---

### Task 2: 必输21点引擎

**Files:**
- Create: `game_engines/grab21.py`
- Test: `tests/test_grab21.py`

- [ ] **Step 1: 写失败测试**

```python
from game_engines import grab21


def test_new_game_initial_state():
    state = grab21.new_game()
    assert state["total"] == 0
    assert state["phase"] == "choose_start"
    assert state["finished"] is False


def test_first_move_creates_total_three():
    state = grab21.new_game()
    state, response = grab21.apply_action(state, "move", "1")
    assert response["valid"] is True
    assert state["total"] == 3
    assert state["history"][0] == {"player": 1, "computer": 2}


def test_invalid_move_rejected():
    state = grab21.new_game()
    state, response = grab21.apply_action(state, "move", "3")
    assert response["valid"] is False


def test_full_game_computer_wins_at_21():
    state = grab21.new_game()
    state, _ = grab21.apply_action(state, "move", "1")
    turn = 0
    while not state["finished"]:
        state, response = grab21.apply_action(state, "move", "2" if turn % 2 else "1")
        assert response["valid"] is True
        turn += 1
        assert turn < 20
    assert state["finished"] is True
    assert state["winner"] == "computer"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_grab21.py -q`

Expected: FAIL，`ModuleNotFoundError: No module named 'game_engines.grab21'`

- [ ] **Step 3: 实现 grab21.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_grab21.py -q`

Expected: `4 passed`

- [ ] **Step 5: 提交**

```bash
git add game_engines/grab21.py tests/test_grab21.py
git commit -m "feat: add grab 21 engine"
```

---

### Task 3: 绝密2025引擎

**Files:**
- Create: `game_engines/codebreaker.py`
- Test: `tests/test_codebreaker.py`

- [ ] **Step 1: 写失败测试**

```python
from game_engines import codebreaker


def test_new_game_has_secret_and_eight_tries():
    state = codebreaker.new_game()
    assert len(state["secret"]) == 4
    assert len(set(state["secret"])) == 4
    assert state["attempts_left"] == 8
    assert codebreaker.public_state(state).get("secret") is None


def test_invalid_guess_rejected():
    state = codebreaker.new_game()
    state, response = codebreaker.apply_action(state, "guess", "1123")
    assert response["valid"] is False
    state, response = codebreaker.apply_action(state, "guess", "12")
    assert response["valid"] is False
    state, response = codebreaker.apply_action(state, "guess", "0123")
    assert response["valid"] is False


def test_correct_guess_wins():
    state = codebreaker.new_game()
    guess = "".join(str(d) for d in state["secret"])
    state, response = codebreaker.apply_action(state, "guess", guess)
    assert response["valid"] is True
    assert state["finished"] is True
    assert state["won"] is True


def test_feedback_counts_a_and_b():
    state = codebreaker.new_game()
    secret = state["secret"]
    wrong_position = [secret[1], secret[0], secret[3], secret[2]]
    state, response = codebreaker.apply_action(state, "guess", "".join(map(str, wrong_position)))
    assert state["guesses"][-1]["feedback"] == "0A4B"


def test_eight_tries_loses():
    state = codebreaker.new_game()
    guess = "1234"
    if "".join(str(d) for d in state["secret"]) == guess:
        guess = "5678"
    for _ in range(8):
        state, response = codebreaker.apply_action(state, "guess", guess)
    assert state["finished"] is True
    assert state["won"] is False
    assert "正确密码" in response["message"]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_codebreaker.py -q`

Expected: FAIL，`ModuleNotFoundError: No module named 'game_engines.codebreaker'`

- [ ] **Step 3: 实现 codebreaker.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_codebreaker.py -q`

Expected: `5 passed`

- [ ] **Step 5: 提交**

```bash
git add game_engines/codebreaker.py tests/test_codebreaker.py
git commit -m "feat: add codebreaker engine"
```

---

### Task 4: 地下城勇士引擎

**Files:**
- Create: `game_engines/dungeon.py`
- Test: `tests/test_dungeon.py`

- [ ] **Step 1: 写失败测试**

```python
import pytest

from game_engines import dungeon


@pytest.fixture
def fixed_dice(monkeypatch):
    def _set(*values):
        iterator = iter(values)
        monkeypatch.setattr(dungeon, "roll_dice", lambda: next(iterator))

    return _set


def test_new_game_starts_in_lobby():
    state = dungeon.new_game()
    assert state["phase"] == "lobby"
    assert state["player"]["hp"] == 100


def test_start_creates_first_monster(fixed_dice):
    fixed_dice(10)
    state = dungeon.new_game()
    state, response = dungeon.apply_action(state, "start")
    assert response["valid"] is True
    assert state["phase"] == "battle"
    assert state["floor"] == 1
    assert state["monster"]["hp"] == 60


def test_attack_success_damages_monster(fixed_dice):
    fixed_dice(10, 3)
    state = dungeon.new_game()
    state, _ = dungeon.apply_action(state, "start")
    state, response = dungeon.apply_action(state, "attack")
    assert response["valid"] is True
    damage = 35 * (1 + 10 / 100)
    assert state["monster"]["hp"] == 60 - damage


def test_skill_requires_mp_and_heals(fixed_dice):
    fixed_dice(12, 3)
    state = dungeon.new_game()
    state, _ = dungeon.apply_action(state, "start")
    hp_before = state["player"]["hp"]
    mp_before = state["player"]["mp"]
    state, response = dungeon.apply_action(state, "skill")
    assert response["valid"] is True
    assert state["monster"]["hp"] == 20
    assert state["player"]["hp"] == hp_before + 40
    assert state["player"]["mp"] == mp_before - 10


def test_run_success_returns_to_camp(fixed_dice):
    fixed_dice(9)
    state = dungeon.new_game()
    state, _ = dungeon.apply_action(state, "start")
    state, response = dungeon.apply_action(state, "run")
    assert response["valid"] is True
    assert state["phase"] == "camp"
    assert state["monster"] is None


def test_death_returns_to_lobby(fixed_dice):
    fixed_dice(3, 9)
    state = dungeon.new_game()
    state, _ = dungeon.apply_action(state, "start")
    state["player"]["hp"] = 5
    state, response = dungeon.apply_action(state, "attack")
    assert response["valid"] is True
    assert state["phase"] == "lobby"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_dungeon.py -q`

Expected: FAIL，`ModuleNotFoundError: No module named 'game_engines.dungeon'`

- [ ] **Step 3: 实现 dungeon.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_dungeon.py -q`

Expected: `7 passed`

- [ ] **Step 5: 提交**

```bash
git add game_engines/dungeon.py tests/test_dungeon.py
git commit -m "feat: add dungeon engine"
```

---

### Task 5: FastAPI 应用与会话

**Files:**
- Create: `app.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: 写失败测试**

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_api.py -q`

Expected: FAIL，`ModuleNotFoundError: No module named 'app'`

- [ ] **Step 3: 实现 app.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_api.py -q`

Expected: `7 passed`

- [ ] **Step 5: 提交**

```bash
git add app.py tests/test_api.py
git commit -m "feat: add fastapi game api"
```

---

### Task 6: 前端静态页面与样式

**Files:**
- Modify: `static/index.html`（替换占位内容）
- Create: `static/style.css`

- [ ] **Step 1: 替换 static/index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>勇者集结 · 四款小游戏</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="app">
    <section id="view-hub" class="view active" data-view="hub">
      <header class="hub-hero">
        <p class="eyebrow">WOLIN ARCADE</p>
        <h1>勇者集结</h1>
        <p class="hub-sub">四款小游戏，一次玩个够</p>
      </header>
      <div class="hub-grid">
        <button class="game-card history" data-game="history">
          <span class="card-index">01</span>
          <strong>野史冲浪</strong>
          <span class="card-tag">历史答题</span>
        </button>
        <button class="game-card grab21" data-game="grab21">
          <span class="card-index">02</span>
          <strong>必输21点</strong>
          <span class="card-tag">先到21者胜</span>
        </button>
        <button class="game-card codebreaker" data-game="codebreaker">
          <span class="card-index">03</span>
          <strong>绝密2025</strong>
          <span class="card-tag">8次破译密码</span>
        </button>
        <button class="game-card dungeon" data-game="dungeon">
          <span class="card-index">04</span>
          <strong>地下城勇士</strong>
          <span class="card-tag">骰子判定冒险</span>
        </button>
      </div>
    </section>

    <section id="view-game" class="view" data-view="game">
      <header class="game-header">
        <button id="back-btn" class="icon-btn" aria-label="返回大厅">←</button>
        <h2 id="game-title"></h2>
        <span id="game-badge" class="game-badge"></span>
      </header>
      <div id="game-content"></div>
    </section>
  </main>
  <div id="toast" class="toast" hidden></div>
  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: 创建 static/style.css**

```css
:root {
  --bg: #0e2b2b;
  --panel: #173d3b;
  --panel-2: #1c413c;
  --line: #4f8a7e;
  --text: #f2e9cf;
  --muted: #a9d8c9;
  --amber: #e8a44d;
  --coral: #ff9d8a;
  --mint: #7fe3b2;
  --sky: #8fd8ff;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at 50% 0%, #143a37 0%, #0e2b2b 55%, #0a2020 100%);
  color: var(--text);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}

.app { max-width: 1080px; margin: 0 auto; padding: 24px 16px 48px; }
.view { display: none; }
.view.active { display: block; }

.hub-hero { text-align: center; padding: 36px 16px 24px; border-bottom: 1px solid var(--line); margin-bottom: 28px; }
.eyebrow { color: var(--mint); font-size: 12px; text-transform: uppercase; margin: 0 0 8px; letter-spacing: 0; }
h1 { margin: 0; font-size: clamp(32px, 6vw, 56px); color: var(--amber); }
.hub-sub { color: var(--muted); margin: 8px 0 0; }

.hub-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.game-card {
  display: flex; flex-direction: column; gap: 8px; align-items: flex-start;
  background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  color: var(--text); padding: 20px; cursor: pointer; text-align: left;
  transition: transform .15s ease, border-color .15s ease;
}
.game-card:hover { transform: translateY(-3px); border-color: var(--amber); }
.game-card strong { font-size: 22px; }
.card-index { color: var(--mint); font-size: 12px; }
.card-tag { color: var(--muted); font-size: 13px; }
.game-card.history { box-shadow: inset 3px 0 0 var(--coral); }
.game-card.grab21 { box-shadow: inset 3px 0 0 var(--mint); }
.game-card.codebreaker { box-shadow: inset 3px 0 0 var(--amber); }
.game-card.dungeon { box-shadow: inset 3px 0 0 var(--sky); }

.game-header { display: flex; align-items: center; gap: 12px; padding-bottom: 14px; border-bottom: 1px solid var(--line); margin-bottom: 20px; }
.game-header h2 { margin: 0; font-size: 24px; }
.game-badge { margin-left: auto; color: var(--muted); font-size: 13px; }
.icon-btn {
  background: var(--panel); border: 1px solid var(--line); color: var(--text);
  border-radius: 6px; width: 40px; height: 40px; font-size: 20px; cursor: pointer;
}
.icon-btn:hover { border-color: var(--amber); }

.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; margin-bottom: 14px; }
.stats { display: flex; flex-wrap: wrap; gap: 10px; }
.stat { background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; padding: 8px 12px; font-size: 14px; }

.question { font-size: 18px; line-height: 1.6; margin: 0 0 16px; }
.options { display: grid; gap: 10px; }
.option-btn {
  background: var(--panel-2); color: var(--text); border: 1px solid var(--line);
  border-radius: 6px; padding: 12px 14px; text-align: left; font-size: 15px; cursor: pointer;
}
.option-btn:hover { border-color: var(--mint); }

.action-row { display: flex; flex-wrap: wrap; gap: 10px; }
.btn {
  background: var(--amber); color: #231303; border: none; border-radius: 6px;
  padding: 12px 18px; font-size: 15px; font-weight: 700; cursor: pointer;
}
.btn:hover { filter: brightness(1.08); }
.btn.ghost { background: transparent; color: var(--muted); border: 1px solid var(--line); }
.btn.coral { background: var(--coral); color: #3a120d; }
.btn.mint { background: var(--mint); color: #0c3a2a; }
.btn:disabled { opacity: .5; cursor: not-allowed; }

.input {
  background: var(--panel-2); border: 1px solid var(--line); color: var(--text);
  border-radius: 6px; padding: 12px; font-size: 16px; width: 160px;
}
.guess-row { display: flex; gap: 10px; align-items: center; }
.guess-list { display: grid; gap: 8px; margin-top: 14px; }
.guess-item {
  display: flex; justify-content: space-between; background: var(--panel-2);
  border: 1px solid var(--line); border-radius: 6px; padding: 10px 12px;
}

.feedback { white-space: pre-line; color: var(--muted); line-height: 1.6; }
.toast {
  position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%);
  background: var(--panel-2); border: 1px solid var(--amber); color: var(--text);
  border-radius: 8px; padding: 12px 18px; max-width: min(90vw, 560px); z-index: 10;
  box-shadow: 0 8px 24px rgba(0, 0, 0, .4); white-space: pre-line;
}
.result { font-size: 20px; font-weight: 700; color: var(--amber); }
```

- [ ] **Step 3: 冒烟验证**

Run:

```powershell
python -m uvicorn app:app --port 5000
```

另开终端运行：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/ -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

Expected: `200`，页面源码包含 `勇者集结`。

- [ ] **Step 4: 提交**

```bash
git add static/index.html static/style.css
git commit -m "feat: add game hub static shell"
```

---

### Task 7: 前端交互脚本

**Files:**
- Create: `static/app.js`

- [ ] **Step 1: 创建 static/app.js**

```javascript
const API_BASE = "";

let current = { game: null, sessionId: null, state: null };
let toastTimer = null;

const GAME_TITLES = {
  history: ["野史冲浪", "历史答题"],
  grab21: ["必输21点", "先到21者胜"],
  codebreaker: ["绝密2025", "8次破译密码"],
  dungeon: ["地下城勇士", "骰子判定冒险"],
};

async function apiCall(game, path, body) {
  const options = body
    ? {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    : { method: "GET" };
  const res = await fetch(`${API_BASE}/api/games/${game}${path}`, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || "请求失败，请重试");
  }
  return data;
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.hidden = true;
  }, 4000);
}

function showView(name) {
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.toggle("active", view.dataset.view === name);
  });
}

function statsRow(items) {
  const row = document.createElement("div");
  row.className = "stats";
  items.forEach((text) => {
    const stat = document.createElement("div");
    stat.className = "stat";
    stat.textContent = text;
    row.appendChild(stat);
  });
  return row;
}

function actionButton(text, action, className = "") {
  const button = document.createElement("button");
  button.className = `btn ${className}`.trim();
  button.dataset.action = action;
  button.textContent = text;
  return button;
}

function restartButton() {
  const button = actionButton("再来一局", "restart", "mint");
  return button;
}

function renderHistory(state) {
  const wrap = document.createElement("div");
  wrap.appendChild(statsRow([`第 ${state.question_index + 1} / ${state.total} 题`, `得分 ${state.score}`]));
  const panel = document.createElement("section");
  panel.className = "panel";
  const question = document.createElement("p");
  question.className = "question";
  question.textContent = state.current_question.question;
  panel.appendChild(question);
  const options = document.createElement("div");
  options.className = "options";
  state.current_question.options.forEach((text, index) => {
    const button = document.createElement("button");
    button.className = "option-btn";
    button.dataset.action = "choose";
    button.dataset.value = String(index + 1);
    button.textContent = `${index + 1}. ${text}`;
    options.appendChild(button);
  });
  panel.appendChild(options);
  wrap.appendChild(panel);
  if (state.finished) {
    const result = document.createElement("div");
    result.className = "panel result";
    result.textContent = `最终得分：${state.score} / ${state.total}`;
    wrap.appendChild(result);
    wrap.appendChild(restartButton());
  }
  return wrap;
}

function renderGrab21(state) {
  const wrap = document.createElement("div");
  const status = state.finished
    ? state.winner === "player"
      ? "你赢了"
      : "独孤木赢了"
    : "你的回合";
  wrap.appendChild(statsRow([`当前数字 ${state.total}`, status]));
  const panel = document.createElement("section");
  panel.className = "panel";
  const prompt = document.createElement("p");
  prompt.className = "question";
  prompt.textContent = state.finished
    ? "本局结束"
    : state.total === 0
      ? "请先报出 1 或 2："
      : "请加 1 或 2：";
  panel.appendChild(prompt);
  if (!state.finished) {
    const row = document.createElement("div");
    row.className = "action-row";
    [1, 2].forEach((num) => {
      const button = actionButton(`+${num}`, "move");
      button.dataset.value = String(num);
      row.appendChild(button);
    });
    panel.appendChild(row);
  }
  wrap.appendChild(panel);
  if (state.history.length) {
    const list = document.createElement("div");
    list.className = "guess-list";
    state.history.forEach((round) => {
      const item = document.createElement("div");
      item.className = "guess-item";
      item.innerHTML = `<span>你 +${round.player}</span><span>独孤木 +${round.computer}</span>`;
      list.appendChild(item);
    });
    wrap.appendChild(list);
  }
  if (state.finished) {
    wrap.appendChild(restartButton());
  }
  return wrap;
}

function renderCodebreaker(state) {
  const wrap = document.createElement("div");
  wrap.appendChild(statsRow([`剩余 ${state.attempts_left} 次`, `已猜 ${state.guesses.length} 次`]));
  const panel = document.createElement("section");
  panel.className = "panel";
  const prompt = document.createElement("p");
  prompt.className = "question";
  prompt.textContent = state.finished
    ? state.won
      ? "破译成功！"
      : "破译失败"
    : "输入 4 位不重复数字（1-9）：";
  panel.appendChild(prompt);
  if (!state.finished) {
    const row = document.createElement("div");
    row.className = "guess-row";
    const input = document.createElement("input");
    input.className = "input";
    input.id = "guess-input";
    input.inputMode = "numeric";
    input.maxLength = 4;
    input.placeholder = "例如 1234";
    const submit = actionButton("提交", "guess");
    submit.dataset.input = "#guess-input";
    row.append(input, submit);
    panel.appendChild(row);
  }
  wrap.appendChild(panel);
  if (state.guesses.length) {
    const list = document.createElement("div");
    list.className = "guess-list";
    [...state.guesses].reverse().forEach((guess) => {
      const item = document.createElement("div");
      item.className = "guess-item";
      item.innerHTML = `<span>${guess.guess}</span><span>${guess.feedback}</span>`;
      list.appendChild(item);
    });
    wrap.appendChild(list);
  }
  if (state.finished) {
    wrap.appendChild(restartButton());
  }
  return wrap;
}

function renderDungeon(state) {
  const wrap = document.createElement("div");
  const player = state.player;
  wrap.appendChild(
    statsRow([
      `HP ${Math.round(player.hp)}`,
      `MP ${Math.round(player.mp)}`,
      `攻击 ${player.attack}`,
      `层数 ${state.floor}`,
    ])
  );
  const panel = document.createElement("section");
  panel.className = "panel";
  const prompt = document.createElement("p");
  prompt.className = "question";
  if (state.phase === "lobby") {
    prompt.textContent = "欢迎来到地下城，开始你的冒险吧。";
  } else if (state.phase === "camp") {
    prompt.textContent = `你通关了第 ${state.floor} 层，准备下一层……`;
  } else {
    prompt.textContent = `遭遇怪物！怪物 HP：${Math.round(state.monster.hp)}，怪物攻击：${state.monster.attack}`;
  }
  panel.appendChild(prompt);
  const row = document.createElement("div");
  row.className = "action-row";
  if (state.phase === "lobby") {
    row.appendChild(actionButton("开始游戏", "start", "mint"));
    row.appendChild(actionButton("退出", "quit", "ghost"));
  } else if (state.phase === "camp") {
    row.appendChild(actionButton("进入下一层", "next_floor", "mint"));
    row.appendChild(actionButton("返回地城入口", "quit", "ghost"));
  } else if (state.phase === "battle") {
    row.appendChild(actionButton("攻击", "attack", "coral"));
    row.appendChild(actionButton("技能", "skill", "mint"));
    row.appendChild(actionButton("逃跑", "run", "ghost"));
  }
  panel.appendChild(row);
  wrap.appendChild(panel);
  return wrap;
}

function errorPanel(message) {
  const panel = document.createElement("section");
  panel.className = "panel";
  const text = document.createElement("p");
  text.className = "feedback";
  text.textContent = message;
  panel.appendChild(text);
  panel.appendChild(restartButton());
  return panel;
}

function render() {
  const content = document.querySelector("#game-content");
  const renderers = {
    history: renderHistory,
    grab21: renderGrab21,
    codebreaker: renderCodebreaker,
    dungeon: renderDungeon,
  };
  content.innerHTML = "";
  content.appendChild(renderers[current.game](current.state));
}

async function startGame() {
  try {
    const data = await apiCall(current.game, "/new", {});
    current.sessionId = data.session_id;
    current.state = data.state;
    render();
  } catch (error) {
    const content = document.querySelector("#game-content");
    content.innerHTML = "";
    content.appendChild(errorPanel(error.message));
  }
}

async function sendAction(action, value) {
  try {
    const data = await apiCall(current.game, "/action", {
      session_id: current.sessionId,
      action,
      value,
    });
    current.state = data.state;
    showToast(data.response.message);
    render();
  } catch (error) {
    showToast(error.message);
  }
}

async function openGame(game) {
  current = { game, sessionId: null, state: null };
  document.querySelector("#game-title").textContent = GAME_TITLES[game][0];
  document.querySelector("#game-badge").textContent = GAME_TITLES[game][1];
  showView("game");
  await startGame();
}

document.querySelectorAll("[data-game]").forEach((card) => {
  card.addEventListener("click", () => openGame(card.dataset.game));
});

document.querySelector("#back-btn").addEventListener("click", () => {
  current = { game: null, sessionId: null, state: null };
  showView("hub");
});

document.querySelector("#game-content").addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  if (button.dataset.action === "restart") {
    startGame();
    return;
  }
  let value = button.dataset.value;
  if (button.dataset.input) {
    const input = document.querySelector(button.dataset.input);
    if (input) value = input.value;
  }
  sendAction(button.dataset.action, value);
});
```

- [ ] **Step 2: 冒烟验证**

启动服务：

```powershell
python -m uvicorn app:app --port 5000
```

另开终端运行：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/ -UseBasicParsing | Select-Object -ExpandProperty Content
```

Expected: HTML 包含 `app.js` 和 `style.css`。随后在浏览器打开 `http://127.0.0.1:5000`，确认四个卡片可以进入游戏、可以返回大厅。

- [ ] **Step 3: 提交**

```bash
git add static/app.js
git commit -m "feat: add game hub frontend interactions"
```

---

### Task 8: 集成验证与指南更新

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: 运行全部测试**

Run: `python -m pytest -q`

Expected: `28 passed`（5 + 4 + 5 + 7 + 7）

- [ ] **Step 2: 验证命令行版本仍可导入**

Run: `python -c "import new_game; print('cli ok')"`

Expected: `cli ok`

- [ ] **Step 3: 验证 API 端到端**

启动服务：

```powershell
python -m uvicorn app:app --port 5000
```

另开终端运行：

```powershell
$r = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/games/history/new
$r.state.current_question.question
```

Expected: 输出第一道历史题的题干。

- [ ] **Step 4: 更新 AGENTS.md**

将 `AGENTS.md` 替换为以下内容：

```markdown
# Repository Guidelines

This repository is a Python console game collection with a FastAPI web frontend. `new_game.py` remains the CLI entry point, while `app.py` serves the same four games in the browser: history quiz, "21" game, code-breaking, and dungeon adventure.

## Project Structure & Module Organization

- `new_game.py`: CLI version of all four games; keep it runnable.
- `app.py`: FastAPI app that exposes the JSON API and hosts the frontend.
- `game_engines/`: pure Python state machines used by the API; no `input()` or `print()`.
- `static/`: `index.html`, `style.css`, `app.js` single-page frontend.
- `tests/`: pytest tests for engines and the API.
- `requirements.txt`: runtime and test dependencies.

## Build, Test, and Development Commands

- `pip install -r requirements.txt` — install dependencies.
- `python -m uvicorn app:app --reload --port 5000` — start the web app.
- `python new_game.py` — run the CLI version.
- `python -m pytest` — run all tests.

## Coding Style & Naming Conventions

Follow PEP 8 for Python: 4-space indentation, snake_case functions and variables, PascalCase classes. JavaScript uses 2-space indentation and `const` by default. Save source as UTF-8. User-facing strings are Chinese and should keep the existing tone. Use comments only where intent is not obvious. No formatter is configured; adopt `black` and `ruff` for Python if the project grows.

## Testing Guidelines

Use `pytest`. Engine tests live in `tests/test_<engine>.py`, API tests in `tests/test_api.py`. Name test methods `test_<behavior>` (for example, `test_invalid_guess_rejected`). Engines must stay free of `input()` and `print()` so rules can be tested without console interaction; dice randomness in the dungeon engine is controlled via monkeypatching `roll_dice`.

## Commit & Pull Request Guidelines

Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`), keep subjects under 72 characters and imperative (for example, `feat: add grab 21 engine`). Before opening a pull request, verify the web app runs, run the full test suite, and include output or screenshots for user-visible changes.

## Security & Configuration Tips

Never commit secrets or machine-specific paths. API sessions live in memory and reset when the server restarts; the code-breaking engine never sends the secret password to the client. Validate player input in the engine layer and return Chinese error messages.
```

- [ ] **Step 5: 提交**

```bash
git add AGENTS.md
git commit -m "docs: update repository guidelines for web app"
```

- [ ] **Step 6: 最终检查**

Run: `python -m pytest -q`

Expected: `28 passed`，无失败。
