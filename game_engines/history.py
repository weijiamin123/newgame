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
