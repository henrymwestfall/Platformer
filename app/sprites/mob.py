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
        self.acc = 1000

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.attack_cooldown = 0.4
        self.last_attack = 0
        
        self.health = 50

        self.move_dir = 0

        self.target = None

        self.hitbox = HitBox(self, self.rect.x, self.rect.y, self.rect.width, self.rect.height, 0, 2000, 5, 500)

    def set_target(self, new_target):
        self.target = new_target

    def handle_jumping(self):
        pass

    def handle_horz_movement(self, dt):
        self.move_dir = 0

        if self.knockback_time != 0:
            return

        if self.target.rect.centerx >= self.rect.centerx: # move right
            self.move_dir = 1
        else:
            self.move_dir = -1

        platform_to_left = False
        platform_to_right = False

        left_look = (self.rect.left - self.rect.width, self.rect.bottom)
        right_look = (self.rect.right + self.rect.width, self.rect.bottom)

        for static_body in self.scene.platform_columns[self.rect.left // 64]:
            if static_body.rect.collidepoint(left_look):
                platform_to_left = True
            elif static_body.rect.collidepoint(right_look):
                platform_to_right = True
            if platform_to_left and platform_to_right:
                break

        if (not platform_to_left) and (not platform_to_right):
            self.move_dir = 0  
        elif not platform_to_left:
            self.move_dir = 1
        elif not platform_to_right:
            self.move_dir = -1

        if self.move_dir == 1:
            self.vel.x = min([self.vel.x + self.acc * dt, self.speed])
        elif self.move_dir == -1:
            self.vel.x = max([self.vel.x - self.acc * dt, -self.speed])
        elif self.vel.x > 0:
            self.vel.x = min([self.vel.x + self.acc * dt, self.speed])
        elif self.vel.x < 0:
            self.vel.x = max([self.vel.x - self.acc * dt, self.speed])


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
        super().update(dt, t)

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