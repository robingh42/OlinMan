import pygame
pygame.init()

class Nonmovable(pygame.sprite.Sprite):
    def __init__(self,points):
        _points = points


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
