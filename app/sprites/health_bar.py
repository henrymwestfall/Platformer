import pygame as pg

from colors import *

class HealthBar(pg.sprite.DirtySprite):
    def __init__(self, scene, x, y):
        super().__init__(scene.hud)

        self.scene = scene

        self.image = pg.Surface([300, 20])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, t):
        self.current_score = self.scene.player.score

        self.image.fill(RED)
        rect = pg.Rect(self.rect)
        width = (self.scene.player.health / self.scene.player.max_health) * rect.width
        rect.width = int(width)
        rect.left = self.rect.left
        pg.draw.rect(self.image, FOREST_GREEN, rect)