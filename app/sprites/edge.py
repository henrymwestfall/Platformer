import pygame as pg

from .foundation import StaticBody
from colors import *

class Edge(pg.sprite.DirtySprite):
    def __init__(self, scene, x, y, width, height):
        super().__init__()

        self.scene = scene
        self.scene.edges.add(self)
        self.image = pg.Surface([width, height])
        self.image.fill(RED)
        pg.draw.line(self.image, BLACK, (0, 0), (width, height))
        pg.draw.line(self.image, BLACK, (width, 0), (0, height))
        self.rect = pg.Rect(x, y, width, height)
        self.player = self.scene.player
        self.colliding_player = False

    def update(self, dt, t):
        if self.rect.colliderect(self.player.rect):
            self.colliding_player = True