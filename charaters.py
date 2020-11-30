import pygame

class Moveable_player(pygame.sprite.Sprite):
    def __init__(self):
        self._x
        self._y
        self._box_x
        self._box_y

    def collision(self):
        pass


class OlinMan(Moveable_player):
    def __init__(self):
        pass


# Enemies to avoid
class Ghost(Moveable_player):

    def __init__(self):
        self._is_chase
        pass

    def frightened(self):
        pass

    def find_target(self):
        pass

    def move(self):
        pass

class blinky(Ghost):
    def __init__(self):
        pass


class pinky(Ghost):
    def __init__(self):
        pass
    

class inky(Ghost):
    def __init__(self):
        pass


class clyde(Ghost):
    def __init__(self):
        pass
