import math

import pygame as pg

from colors import *
from .foundation import RigidBody
from .collectables import Coin
from .hitbox import HitBox
from .character import Character


class Player(Character):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y, 32, 52, fill_color=SKY_BLUE)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 400
        self.acc = self.speed * 4

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.climb = 250

        self.attack_cooldown = 0.2
        self.mouse_has_lifted = True

        self.score = 0

        self.move_dir = 0

        self.max_health = 100
        self.health = self.max_health

        screen_w = self.scene.screen.get_width()
        screen_h = self.scene.screen.get_height()
        self.hitbox_calculation_lines = (
            lambda x, shift: (screen_h / screen_w) * (x - shift), # top left to bottom right
            lambda x, shift: -(screen_h / screen_w) * (x - shift) + screen_h # bottom left to top right
        )
        self.hitbox_length = int(self.rect.height * 2.5) # long side of the hitbox
        self.hitbox_width = int(self.rect.width * 2.5) # short side of the hitbox

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

    def handle_horz_movement(self, dt):
        self.moving = False
        self.move_dir = 0

        self.being_knocked_back = (not self.landed) and self.being_knocked_back

        if self.being_knocked_back:
            return

        if self.scene.keys_pressed[pg.K_d] ^ self.scene.keys_pressed[pg.K_a]:
            if self.scene.keys_pressed[pg.K_d]: # move right
                self.move_dir = 1
                self.vel.x = min([self.vel.x + self.acc * dt, self.speed])
            elif self.scene.keys_pressed[pg.K_a]:
                self.move_dir = -1
                self.vel.x = max([self.vel.x - self.acc * dt, -self.speed])

    def handle_attack(self, t):
        if self.scene.mouse_state[0] and self.mouse_has_lifted and t - self.last_attack >= self.attack_cooldown: # left click
            mp = self.scene.get_window_mouse_pos()
            tl_br, bl_tr = self.hitbox_calculation_lines

            shift = (pg.math.Vector2(self.scene.camera.shifted_rect(self.rect).center) - self.scene.screen_rect.center)

            mouse_pos_test_results = (
                mp.y <= tl_br(mp.x, shift.x) + shift.y and mp.y <= bl_tr(mp.x, shift.x) + shift.y,  # bottom quadrant
                mp.y >= tl_br(mp.x, shift.x) + shift.y and mp.y <= bl_tr(mp.x, shift.x) + shift.y, # right quadrant
                mp.y <= tl_br(mp.x, shift.x) + shift.y and mp.y >= bl_tr(mp.x, shift.x) + shift.y, # left quadrant
                mp.y >= tl_br(mp.x, shift.x) + shift.y and mp.y >= bl_tr(mp.x, shift.x) + shift.y # top quadrant
            )

            for quadrant, result in enumerate(mouse_pos_test_results):
                if result == True:
                    break
            else:
                print("Warning: mouse position failed all tests. Debugging necessary.")
                return
            
            if quadrant == 0: # top quadrant
                HitBox(self, self.rect.centerx - self.hitbox_length // 2, self.rect.top - self.hitbox_width, self.hitbox_length, self.hitbox_width, t, 0.05, 20, 500, color=WHITE)
            elif quadrant == 1: # left quadrant
                HitBox(self, self.rect.left - self.hitbox_width, self.rect.centery - self.hitbox_length // 2, self.hitbox_width, self.hitbox_length, t, 0.05, 20, 500, color=WHITE)
            elif quadrant == 2: # right quadrant
                HitBox(self, self.rect.right, self.rect.centery - self.hitbox_length // 2, self.hitbox_width, self.hitbox_length, t, 0.05, 20, 500, color=WHITE)
            else: # bottom quadrant
                HitBox(self, self.rect.centerx - self.hitbox_length // 2,  self.rect.bottom, self.hitbox_length, self.hitbox_width, t, 0.05, 20, 500, color=WHITE)

            self.last_attack = t
        
        self.mouse_has_lifted = not self.scene.mouse_state[0]

    def update(self, dt, t):
        super().update(dt, t)

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
        self.handle_horz_movement(dt)

        # apply friction
        self.apply_friction()

        # handle attack
        self.handle_attack(t)
        
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