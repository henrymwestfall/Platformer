import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .collectables import Coin
from .hitbox import HitBox
from .character import Character


class Mob(Character):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y, 32, 52, fill_color=RED)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 250
        self.acc = 500

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.attack_cooldown = 0.4
        self.last_attack = 0
        
        self.health = 200

        self.move_dir = 0

        self.target = None

        self.hitbox = HitBox(self, self.rect.x, self.rect.y, self.rect.width, self.rect.height, 0, 2000, 10, 500, color=RED)

    def set_target(self, new_target):
        self.target = new_target

    def handle_jumping(self):
        pass

    def handle_horz_movement(self, dt):
        self.move_dir = 0
        
        self.being_knocked_back = (not self.landed) and self.being_knocked_back

        if self.being_knocked_back:
            return

        if self.target.rect.centerx >= self.rect.centerx: # move right
            self.move_dir = 1
            self.vel.x = min([self.vel.x + self.acc * dt, self.speed])
        else:
            self.move_dir = -1
            self.vel.x = max([self.vel.x - self.acc * dt, -self.speed])

        pt = self.rect.bottom + self.vel.x + 5
        for body in self.scene.static_bodies:
            if body.rect.collidepoint((pt, self.rect.centerx)):
                break
        else:
            pass

    def handle_attack(self, t):
        if t - self.last_attack >= self.attack_cooldown: # left click
            y = self.rect.top
            if self.target.rect.centerx >= self.rect.right:
                x = self.rect.right
            else:
                x = self.rect.left - self.rect.width
            HitBox(self, x, y, self.rect.width, self.rect.height, t, 0.05, 20, 1000, color=WHITE)

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
        self.handle_horz_movement(dt)

        # apply friction
        self.apply_friction()

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

        if self.health <= 0:
            self.kill()
            self.hitbox.kill()