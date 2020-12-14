import pytest
import olin_man_game
import characters
import objects

directions = [
    ("up", False),
    ("down", False),
    ("left", True),
    ("right", True)]


@pytest.mark.parametrize("direction, bool_check", directions)
def test_can_move(direction, bool_check):
    state = olin_man_game.Game_State()
    player = charaters.OlinMan(state,1)
    player.move(direction)
    assert player.can_move() == bool_check
