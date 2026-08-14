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
