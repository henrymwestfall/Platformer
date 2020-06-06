import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .collectables import Coin


class Player(RigidBody):
    def __init__(self, scene, x, y):
        RigidBody.__init__(self, scene)

        self.image = pg.Surface([32, 52])
        self.image.fill(BLUE)
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

        self.climb = 250

        self.score = 0

    def update(self, dt, t):
        landed = len(self.collisions["down"]) > 0
        touching_left = len(self.collisions["left"]) > 0
        touching_right = len(self.collisions["right"]) > 0

        # apply gravity
        if not landed:
            self.vel += pg.math.Vector2(0, self.scene.gravity) * dt

        # jump
        if landed and self.scene.keys_pressed[pg.K_w]:
            self.vel.y = -self.jump_strength
        elif self.vel.y < 0 and not self.scene.keys_pressed[pg.K_w]:
            self.vel.y *= self.jump_cut

        # handle climbing
        
        if not landed and (touching_left or touching_right):
            self.vel.y = 0
            if self.scene.keys_pressed[pg.K_w]:
                self.vel.y = -self.climb
            elif self.scene.keys_pressed[pg.K_s]:
                self.vel.y = self.climb
        
        # move left/right
        self.moving = False

        if self.scene.keys_pressed[pg.K_d] ^ self.scene.keys_pressed[pg.K_a]:
            if self.scene.keys_pressed[pg.K_d]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
                self.moving = True
            elif self.scene.keys_pressed[pg.K_a]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x
                self.moving = True

        if landed and not self.moving:
            friction = self.collisions["down"][0].friction * math.copysign(1, -self.vel.x)
            new_vel_x = self.vel.x + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel_x):
                self.vel.x = new_vel_x
            else:
                self.vel.x = 0

        self.image = pg.Surface([self.rect.width, self.rect.height])
        self.image.fill(SKY_BLUE)
        """
        internal_image = pg.Surface([24, 24])
        if self.moving:
            internal_image.fill(RED)
        else:
            internal_image.fill(BLUE)
        rect = pg.Rect(4, 4, 28, 28)
        self.image.blit(internal_image, rect)"""

        if self.scene.keys_pressed[pg.K_SPACE]:
            self.scene.shake_screen(t, 50, 2)
        
        # update position
        self.move(dt)
        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)
        self.rect.topleft = rect_pos

        collided_rigid_bodies = pg.sprite.spritecollide(self, self.scene.rigid_bodies, False)
        for body in collided_rigid_bodies:
            if isinstance(body, Coin):
                self.score += 1
                body.kill()