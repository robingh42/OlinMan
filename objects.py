import pygame
from pygame.locals import *
from olin_man_game import Viewer

pygame.init()

class Nonmovable(pygame.sprite.Sprite):
    def __init__(self,image ,points=0):
        _points = points
        self.image, self.rect = Viewer.load_image(image)


class snack(Nonmovable):
    def __init__(self):
        super().__init__(10)


class coffee(Nonmovable):
    def __init__(self):
        super().__init__(50)


class wall(Nonmovable):
    def __init__(self):
        super().__init__(0)


class cherry(Nonmovable):
    def __init__(self):
        super().__init__(1000)
