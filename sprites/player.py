import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .collectables import Coin


class Player(RigidBody):
    def __init__(self, scene, x, y):
        RigidBody.__init__(self, scene)

        self.image = pg.Surface([32, 52])
        self.image.fill(SKY_BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 600
        self.acc = 0.1

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.climb = 250

        self.score = 0

        self.landed = False
        self.touching_left = False
        self.touching_right = False
        self.climbing = False

    def apply_gravity(self, dt):
        if not self.landed:
            self.vel += pg.math.Vector2(0, self.scene.gravity) * dt

    def handle_jumping(self):
        if self.landed and self.scene.keys_pressed[pg.K_w]:
            self.vel.y = -self.jump_strength
        elif self.vel.y < 0 and not self.scene.keys_pressed[pg.K_w]:
            self.vel.y *= self.jump_cut

    def handle_climbing(self):
        self.climbing = False
        if not self.landed and (self.touching_left or self.touching_right):
            self.climbing = True
            self.vel.y = 0
            if self.scene.keys_pressed[pg.K_w]:
                self.vel.y = -self.climb
            elif self.scene.keys_pressed[pg.K_s]:
                self.vel.y = self.climb

    def handle_horz_movement(self):
        self.moving = False
        if self.scene.keys_pressed[pg.K_d] ^ self.scene.keys_pressed[pg.K_a]:
            if self.scene.keys_pressed[pg.K_d]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
                self.moving = True
            elif self.scene.keys_pressed[pg.K_a]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x
                self.moving = True

    def apply_friction(self):
        if self.landed and not self.moving:
            friction = self.collisions["down"][0].friction * math.copysign(1, -self.vel.x)
            new_vel_x = self.vel.x + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel_x):
                self.vel.x = new_vel_x
            else:
                self.vel.x = 0

    def update(self, dt, t):
        # update collision variables
        self.landed = len(self.collisions["down"]) > 0
        self.touching_left = len(self.collisions["left"]) > 0
        self.touching_right = len(self.collisions["right"]) > 0

        # apply gravity
        self.apply_gravity(dt)

        # handle jumping
        self.handle_jumping()

        # handle climbing
        self.handle_climbing()
        
        # move left/right
        self.handle_horz_movement()

        # apply friction
        self.apply_friction()
        
        # update position
        self.move(dt)
        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)
        self.rect.topleft = rect_pos

        # handle collisions with collectables and other rigid bodies
        collided_rigid_bodies = pg.sprite.spritecollide(self, self.scene.rigid_bodies, False)
        for body in collided_rigid_bodies:
            if isinstance(body, Coin):
                self.score += 1
                body.kill()