import math

import pygame as pg

from .foundation import RigidBody, StaticBody
from colors import GREEN, RED, BLACK, WHITE

class TestStaticBody(StaticBody):
    def __init__(self, scene, x, y, width):
        StaticBody.__init__(self, scene)

        self.image = pg.Surface([width, 32])
        self.image.fill(BLACK)
        internal_image = pg.Surface([width - 8, 24])
        internal_image.fill(GREEN)
        rect = pg.Rect(4, 4, width - 4, 28)
        self.image.blit(internal_image, rect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.friction = 0.05


class TestRigidBody(RigidBody):
    def __init__(self, scene, x, y):
        RigidBody.__init__(self, scene)

        self.image = pg.Surface([32, 32])
        self.image.fill(BLACK)
        internal_image = pg.Surface([24, 24])
        internal_image.fill(RED)
        rect = pg.Rect(4, 4, 28, 28)
        self.image.blit(internal_image, rect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 600
        self.acc = 0.1

    def update(self, dt, t):
        super().update(dt, t)
        self.pos = pg.math.Vector2(self.rect.topleft)

        if self.landed and self.scene.keys_pressed[pg.K_UP]:
            self.vel += pg.math.Vector2(0, -1600)

        if self.scene.keys_pressed[pg.K_RIGHT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
        if self.scene.keys_pressed[pg.K_LEFT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x

        if self.landed:
            # lerp as if positive
            pos_vel = pg.math.Vector2(self.vel)
            pos_vel.x = abs(pos_vel.x)
            new_x = pos_vel.lerp(pg.math.Vector2(0, 0), self.underneath.friction).x
            self.vel.x = math.copysign(new_x, self.vel.x)

        self.pos += self.vel * dt

        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)

        self.rect.topleft = rect_pos
