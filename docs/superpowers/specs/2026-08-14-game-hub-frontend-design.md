# 游戏合集前端设计文档

日期：2026-08-14

状态：已确认

## 背景与目标

`new_game.py` 是包含四款中文小游戏的控制台程序：野史冲浪、必输21点、绝密2025、地下城勇士。目标是新增一个浏览器前端，让这四款游戏可以在网页上完整游玩，同时保留命令行版本。

## 架构

- `app.py`：FastAPI 应用，提供 JSON API 并托管前端静态文件。
- `game_engines/`：纯 Python 游戏状态机，不直接调用 `input()` 或 `print()`。
  - `history.py`：野史冲浪。
  - `grab21.py`：必输21点。
  - `codebreaker.py`：绝密2025。
  - `dungeon.py`：地下城勇士。
- `static/`：`index.html`、`style.css`、`app.js`，前端不引入第三方库。
- `requirements.txt`：`fastapi`、`uvicorn`，测试另加 `pytest`、`httpx`。
- `tests/`：引擎测试和 API 测试。
- `new_game.py`：保持原样，命令行版本不受影响。

## 引擎接口

每个引擎提供两个统一入口：

- `new_game() -> state`：创建一局，返回 JSON 可序列化的初始状态。
- `apply_action(state, action, value) -> (state, response)`：执行玩家操作，返回新状态和界面数据。

`response` 统一包含 `valid`、`message`、`events`、`finished` 字段，`message` 为中文提示。`valid` 为 `False` 时表示非法输入，API 返回 400。

### 野史冲浪

- 题目、选项、正确答案和反馈文案取自 `new_game.py` 现有内容。
- 状态：当前题号、得分、是否结束。
- 操作：`choose`，参数为选项编号。

### 必输21点

- 玩家与电脑轮流在当前数字上加 1 或 2，先到 21 者胜。
- 状态：当前数字、胜负、是否结束。
- 操作：`move`，参数为 1 或 2；引擎随后计算电脑回合。

### 绝密2025

- 系统生成 4 位不重复数字密码，玩家 8 次机会内猜中即赢。
- 状态：隐藏密码、剩余次数、历史猜测和反馈。
- 操作：`guess`，参数为 4 位不重复数字。

### 地下城勇士

- 掷三次骰子（1-6）判定攻击、技能和逃跑结果，战斗规则沿用 `new_game.py`。
- 状态：玩家 HP/MP/攻击、楼层、怪物、阶段。
- 操作：`enter_floor`、`attack`、`skill`、`run`、`quit`。

## API

统一前缀 `/api/games/<game>`，`game` 取值 `history`、`grab21`、`codebreaker`、`dungeon`。

- `POST /api/games/<game>/new`：创建一局，返回 `session_id` 和初始状态。
- `POST /api/games/<game>/action`：请求体包含 `session_id`、`action`、可选 `value`，返回新状态和响应数据；非法操作返回 400 和中文错误信息。
- `GET /api/games/<game>/state`：按 `session_id` 查询当前状态。

会话保存在内存字典中，键为 UUID。会话不存在时返回 410，前端自动重开一局。

## 前端

- 单页应用，JS 负责视图切换：大厅、野史冲浪、必输21点、绝密2025、地下城勇士。
- 大厅展示四张游戏卡片，点击进入全屏游戏视图，左上角返回。
- 视觉风格为已确认的深夜地下城方向：深青背景、石墙面板、火把暖光，四个游戏分别使用珊瑚红、薄荷绿、琥珀金、天蓝色。
- 移动端优先，桌面端居中展示，所有按钮和反馈均为中文。

## 错误处理

- 引擎层校验玩家输入，返回具体中文提示。
- 前端 `fetch` 失败时显示错误横幅，提供重试和重新开局入口。
- 会话失效时自动创建新会话，避免页面卡死。

## 测试

- 使用 `pytest`，测试文件命名 `test_*.py`。
- 每个引擎至少覆盖胜负规则、非法输入和正常流程。
- API 测试使用 Flask `test_client`，覆盖创建会话、执行操作和错误路径。

## 开发命令

- `pip install -r requirements.txt`：安装依赖。
- `uvicorn app:app --reload --port 5000`：启动本地服务，默认端口 5000。
- `python -m pytest`：运行全部测试。

## 验收标准

- 启动服务后可在浏览器中完整游玩四款游戏。
- `python new_game.py` 仍可正常使用。
- `python -m pytest` 全部通过。

## 不在范围内

- 数据库、多用户、排行榜、音效、离线 PWA。
