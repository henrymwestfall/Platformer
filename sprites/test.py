import math

import pygame as pg

from .foundation import RigidBody, StaticBody, Particle
from colors import *

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

        self.friction = pg.math.Vector2(100, 0)


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

        self.jump_strength = 1000
        self.jump_cut = 0.5

    def update(self, dt, t):
        super().update(dt, t)
        self.pos = pg.math.Vector2(self.rect.topleft)

        # jump
        if self.landed and self.scene.keys_pressed[pg.K_UP]:
            self.vel.y = -self.jump_strength
        elif self.vel.y < 0 and not self.scene.keys_pressed[pg.K_UP]:
            self.vel.y *= self.jump_cut

        # move left/right
        self.moving = False
        if self.scene.keys_pressed[pg.K_RIGHT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
            self.moving = True
        if self.scene.keys_pressed[pg.K_LEFT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x
            self.moving = True
        if self.landed and not self.moving:
            friction = self.underneath.friction * math.copysign(1, -self.vel.x)
            new_vel = self.vel + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel.x):
                self.vel = new_vel
            else:
                self.vel.x = 0
        
        # update position
        self.pos += self.vel * dt
        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)
        self.rect.topleft = rect_pos


class TestParticle(Particle):
    def __init__(self, scene, center, push_vector):
        Particle.__init__(self, scene)

        self.vel = push_vector
        self.radius = 4

        self.image = pg.Surface([self.radius * 2, self.radius * 2])
        pg.draw.circle(self.image, WHITE, center, self.radius)
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.life_time = 1
        self.life = self.life_time

    def update(self, dt, t):
        center = pg.math.Vector2(self.rect.center) + self.vel
        
        #color = pg.Color(255, 255, 255, int(255 * (self.life / self.life_time)))
        radius = int(self.radius * self.life / self.life_time)
        self.image = pg.Surface([radius * 2, radius * 2])
        pg.draw.circle(self.image, WHITE, self.rect.center, radius)
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.life -= dt
        if self.life < 0:
            self.kill()
        