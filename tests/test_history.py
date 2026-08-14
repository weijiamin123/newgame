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
