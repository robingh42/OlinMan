import pytest
import pygame
from pygame.locals import *
import olin_man_game
import characters
vec = pygame.math.Vector2

directions = [
    (vec(0,-1), False),  #up
    (vec(0,1), False),   #down
    (vec(-1,0), True),   #left
    (vec(1,0), True)]    #right


@pytest.mark.parametrize("direction, bool_check", directions)
def test_can_move(direction, bool_check):
    state = olin_man_game.Game_State()
    state.make_walls()
    player = characters.OlinMan(state, 1)
    player.direction = direction
    assert player.can_move() == bool_check

@pytest.mark.parametrize("direction, bool_check", directions)
def test_ghost_can_move(direction, bool_check):
    state = olin_man_game.Game_State()
    state.make_walls()
    player = characters.Ghost(state, [3, 4], 2)
    player.direction = direction
    assert player.can_move() == bool_check

@pytest.mark.parametrize('execution_number', range(20))
def test_ghost_corner(execution_number):
    backwards = False
    state = olin_man_game.Game_State()
    state.make_walls()
    player = characters.Ghost(state, [3, 4], 2)
    player.direction = vec(-1,0)
    for _ in range(20):
        player.update()
        if player.direction == vec(1,0):
            backwards = True
            print(f"Direct: {player.direction}")
    assert not backwards