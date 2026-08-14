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
