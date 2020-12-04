import pygame
from pygame.locals import *

pygame.init()

class MoveablePlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        self._surface = pygame.display.get_surface()

        self._image = pygame.image.load("")
        self._rect = self.image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._speed = speed

    def collision(self):
        pass

    def update(self):
        pass


class OlinMan(MoveablePlayer):

    def __init__(self, lives):
        super.__init__(self, 224, 384, 16)
        self._lives = lives


# Enemies to avoid
class Ghost(MoveablePlayer):

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

    def find_target(self):
        # on Olin Man
        pass


class pinky(Ghost):
    def __init__(self):
        pass

    def find_target(self):
        # 4 squares Olin Man
        pass

class inky(Ghost):
    def __init__(self):
        pass

    def find_target(self):
        # opposite blinky
        pass


class clyde(Ghost):
    def __init__(self):
        pass
