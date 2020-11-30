import pygame

class Nonmovable(pygame.sprite.Sprite):
    def __init__(self,points):
        _points = points


class snack(Nonmovable):
    def __init__(self):
        super().__init__(10)


class coffee(Nonmovable):
    def __init__(self):
        pass


class wall(Nonmovable):
    def __init__(self):
        pass


class cherry(Nonmovable):
    def __init__(self):
        pass
