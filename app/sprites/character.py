import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .hitbox import HitBox


class Character(RigidBody):
    def __init__(
            self, 
            scene, 
            x, 
            y, 
            w, 
            h, 
            speed=0, 
            acc=0, 
            jump_strength=0,
            jump_cut=0,
            attack_cooldown=0.0,
            health=0,
            fill_color=BLACK):

        super().__init__(scene)

        self.image = pg.Surface([w, h])
        self.image.fill(fill_color)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = speed
        self.acc = acc

        self.jump_strength = jump_strength
        self.jump_cut = jump_cut
        
        self.attack_cooldown = attack_cooldown
        self.last_attack = 0

        self.invinsible_time = 0

    def update(self, dt, t):
        self.invinsible_time -= dt
        if self.invinsible_time < 0:
            self.invinsible_time = 0

    def apply_friction(self):
        if self.landed and self.move_dir == 0:
            friction = self.collisions["down"][0].friction * math.copysign(1, -self.vel.x)
            new_vel_x = self.vel.x + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel_x):
                self.vel.x = new_vel_x
            else:
                self.vel.x = 0