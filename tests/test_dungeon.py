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
