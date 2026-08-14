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
