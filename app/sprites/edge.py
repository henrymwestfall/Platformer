import math

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
        self.colliding_player = False
        if self.rect.colliderect(self.player.rect):
            angle = pg.math.Vector2(1, 0).angle_to(self.player.vel)
            w = self.rect.width
            h = w * math.sin(angle)

            new_rect = pg.Rect(self.player.rect)
            new_rect.x += w
            new_rect.y += h

            if self.rect.colliderect(new_rect):
                self.colliding_player = True
                self.player.rect = new_rect
                self.player.pos = pg.math.Vector2(new_rect.topleft)