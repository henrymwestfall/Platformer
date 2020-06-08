import pygame as pg

from .collectables import Coin

class ScoreTracker(pg.sprite.DirtySprite):
    def __init__(self, scene, x, y):
        super().__init__(scene.hud)

        self.scene = scene

        self.max_score = len([body for body in self.scene.rigid_bodies if isinstance(body, Coin)])
        self.current_score = 0

        self.image = pg.Surface([20 * self.max_score, 20])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, t):
        self.current_score = self.scene.player.score

        self.image.fill(pg.Color(0, 0, 0, 0)) # transparent
        for i in range(self.max_score):
            if i < self.current_score:
                pg.draw.circle(self.image, (255, 255, 0), (20 * i + 10, 10), 8)
            else:
                pg.draw.circle(self.image, (121, 121, 121), (20 * i + 10, 10), 8)