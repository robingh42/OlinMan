import pytest
import pygame
from pygame.locals import *
import olin_man_game
import characters
import objects
vec = pygame.math.Vector2

directions = [
    ("up", False),
    ("down", False),
    ("left", True),
    ("right", True)]


@pytest.mark.parametrize("direction, bool_check", directions)
def test_can_move(direction, bool_check):
    state = olin_man_game.Game_State()
    player = characters.OlinMan(state,1)
    player.move(direction)
    assert player.can_move() == bool_check


def test_ghost_corner():
    state = olin_man_game.Game_State()
    player = characters.Ghost(state,[4,3],2)
    player.direction = vec(-1,0)
    player.move()
    assert player.can_move() == True