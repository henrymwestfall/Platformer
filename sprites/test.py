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

        self.friction = pg.math.Vector2(10, 0)


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

        self.long_jump_timer_started = False
        self.jumping = False
        self.jump_start = 0
        self.jump_time = 0.15
        self.jump_decay = 0.9
        self.jump_strength = 200

    def update(self, dt, t):
        super().update(dt, t)
        self.pos = pg.math.Vector2(self.rect.topleft)

        was_jumping = self.jumping
        if (self.landed or self.jumping) and self.scene.keys_pressed[pg.K_UP]:
            self.jumping = True
            if not was_jumping:
                self.jump_start = t
            if (t - self.jump_start) <= self.jump_time:
                self.vel += pg.math.Vector2(0, -self.jump_strength * self.jump_decay ** (t - self.jump_start))
            """
            if not self.long_jump_timer_started:
                pg.time.set_timer(pg.USEREVENT, 100)
                self.long_jump_timer_started = True
            """
        else:
            self.jumping = False

        if self.scene.keys_pressed[pg.K_RIGHT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
        if self.scene.keys_pressed[pg.K_LEFT]:
            self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x

        self.was_landed_last_frame = False
        if self.landed:
            friction = self.underneath.friction * math.copysign(1, -self.vel.x)
            new_vel = self.vel + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel.x):
                self.vel = new_vel
            else:
                self.vel.x = 0

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
        