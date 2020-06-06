import random

import pygame as pg

class Camera:
    def __init__(self, scene, speed, acc, drag):
        self.scene = scene
        self.screen = self.scene.screen
        self.screen_middle = pg.math.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        self.focus = None
        self.speed = speed
        self.acc = acc
        self.drag = drag
        self.shift = pg.math.Vector2(0, 0)

        self.shake_start = 0
        self.shake_duration = 0
        self.shake_magnitude = 0

    def set_focus(self, new_focus):
        self.focus = new_focus

    def shifted_rect(self, absolute_rect):
        rect = pg.Rect(absolute_rect)
        rect.x -= self.shift.x
        rect.y -= self.shift.y
        return rect

    def schedule_shake_screen(self, t, magnitude, duration):
        self.shake_start = t
        self.shake_magnitude = magnitude
        self.shake_duration = duration

    def handle_screenshake(self, t):
        if t - self.shake_start >= self.shake_duration:
            self.shake_duration = 0
        if self.shake_duration > 0:
            choices = [self.shake_magnitude, 0]
            random.shuffle(choices)
            shift = pg.math.Vector2(choices) * random.choice([-1, 1])
            progress = (t - self.shake_start) / self.shake_duration
            shift = shift.lerp(pg.math.Vector2(0, 0), progress)
            self.camera_shift += shift

    def update(self, dt, t):
        if self.focus == None:
            return

        needs_update = False
        if self.focus.rect.centerx < self.screen_middle.x - self.drag:
            needs_update = True
        elif self.focus.rect.centerx > self.screen_middle.x + self.drag:
            needs_update = True

        if self.focus.rect.centery < self.screen_middle.y - self.drag:
            needs_update = True
        elif self.focus.rect.centery > self.screen_middle.y + self.drag:
            needs_update = True
        
        if needs_update:
            self.shift = self.shift.lerp(pg.math.Vector2(self.focus.rect.center) - self.screen_middle, self.acc)
        
        self.handle_screenshake(t)