import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .collectables import Coin
from .hitbox import HitBox


class Mob(RigidBody):
    def __init__(self, scene, x, y):
        super().__init__(scene)

        self.image = pg.Surface([32, 52])
        self.image.fill(RED)
        # draw eyes
        pg.draw.circle(self.image, BLACK, (32 - 8, 8), 4)
        pg.draw.circle(self.image, BLACK, (8, 8), 4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 250
        self.acc = 0.2

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.attack_cooldown = 0.4
        self.last_attack = 0

        self.health = 200

        self.landed = False
        self.touching_left = False
        self.touching_right = False
        self.climbing = False

        self.target = None

    def set_target(self, new_target):
        self.target = new_target

    def apply_gravity(self, dt):
        if not self.landed:
            self.vel += pg.math.Vector2(0, self.scene.gravity) * dt

    def handle_jumping(self):
        pass

    def handle_horz_movement(self):
        if self.target.rect.centerx >= self.rect.centerx:
            self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
        else:
            self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x


    def apply_friction(self):
        if self.landed and not self.moving:
            friction = self.collisions["down"][0].friction * math.copysign(1, -self.vel.x)
            new_vel_x = self.vel.x + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel_x):
                self.vel.x = new_vel_x
            else:
                self.vel.x = 0

    def handle_attack(self, t):
        if t - self.last_attack >= self.attack_cooldown: # left click
            y = self.rect.top
            if self.target.rect.centerx >= self.rect.right:
                x = self.rect.right
            else:
                x = self.rect.left - self.rect.width
            HitBox(self, x, y, self.rect.width, self.rect.height, t, 0.05, 20, 200, color=WHITE)

            self.last_attack = t

    def update(self, dt, t):
        # update collision variables
        self.landed = len(self.collisions["down"]) > 0
        self.touching_left = len(self.collisions["left"]) > 0
        self.touching_right = len(self.collisions["right"]) > 0

        # apply gravity
        self.apply_gravity(dt)

        # handle jumping
        self.handle_jumping()
        
        # move left/right
        self.handle_horz_movement()

        # apply friction
        #self.apply_friction()

        # handle attack
        #self.handle_attack(t)
        
        # update position
        self.move(dt)
        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)
        self.rect.topleft = rect_pos