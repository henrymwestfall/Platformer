import random

import pygame as pg

from colors import *

class Scene:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.game.scenes_by_name[self.name] = self

        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()

        # groups / collision layers
        self.children = pg.sprite.Group() # all child sprites

        self.rigid_bodies = pg.sprite.Group() # affected by gravity
        self.static_bodies = pg.sprite.Group() # immobile platforms
        self.projectiles = pg.sprite.Group() # unaffected by gravity
        self.particles = pg.sprite.Group() # unaffected by anything

        # environment
        self.background = BLACK
        self.gravity = 3000
        self.terminal_velocity = pg.math.Vector2(0, 1250)

        # input
        self.events = []
        self.keys_pressed = []

        # camera
        self.camera_focus = None
        self.camera_speed = 500
        self.camera_acc = 0.05
        self.camera_drag = 25
        self.camera_shift = pg.math.Vector2(0, 0)

        self.screen_shake_start = 0
        self.screen_shake_duration = 0
        self.screen_shake_magnitude = 0

    
    def handle_events(self):
        self.events = pg.event.get()
        self.keys_pressed = pg.key.get_pressed()

    
    def draw(self):
        self.screen.fill(self.background)
        
        # order matters
        self.draw_group(self.static_bodies)
        self.draw_group(self.projectiles)
        self.draw_group(self.rigid_bodies)
        self.draw_group(self.particles)

    def draw_group(self, group):
        for e in group:
            rect = pg.Rect(e.rect)
            rect.x -= self.camera_shift.x
            rect.y -= self.camera_shift.y
            if rect.colliderect(self.screen_rect):
                self.screen.blit(e.image, rect)
                
    def start(self):
        pass

    def update(self, dt, t):
        # update camera
        if self.camera_focus != None:
            middle = pg.math.Vector2(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)

            needs_update = False
            if self.camera_focus.rect.centerx < middle.x - self.camera_drag: # move camera left
                needs_update = True
            elif self.camera_focus.rect.centerx > middle.x + self.camera_drag: # move camera right
                needs_update = True

            if self.camera_focus.rect.centery < middle.y - self.camera_drag: # move camera up
                needs_update = True
            elif self.camera_focus.rect.centery > middle.y + self.camera_drag: # move camera down
                needs_update = True

            if needs_update:
                self.camera_shift = self.camera_shift.lerp(pg.math.Vector2(self.camera_focus.rect.center) - middle, self.camera_acc)

        # screenshake
        if t - self.screen_shake_start >= self.screen_shake_duration:
                self.screen_shake_duration = 0
        if self.screen_shake_duration > 0:
            choices = [self.screen_shake_magnitude, 0]
            random.shuffle(choices)
            shift = pg.math.Vector2(choices) * random.choice([-1, 1])
            progress = (t - self.screen_shake_start) / self.screen_shake_duration
            shift = shift.lerp(pg.math.Vector2(0, 0), progress)

            self.camera_shift += shift
            

        for sprite in self.rigid_bodies:
            sprite.update(dt, t)
        for particle in self.particles:
            particle.update(dt, t)

    def shake_screen(self, t, magnitude, duration):
        self.screen_shake_start = t
        self.screen_shake_magnitude = magnitude
        self.screen_shake_duration = duration

    def close(self):
        pass