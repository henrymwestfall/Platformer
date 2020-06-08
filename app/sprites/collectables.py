import pygame as pg

from .foundation import RigidBody

class Coin(RigidBody):
    def __init__(self, scene, x, y):
        super().__init__(scene)

        self.image = pg.Surface([16, 16])
        pg.draw.circle(self.image, (255, 255, 0), (8, 8), 8)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)