import random

import pygame as pg

class Camera:
    def __init__(self, scene, speed, acc, drag):
        self.scene = scene
        self.screen = self.scene.screen
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.screen_middle = pg.math.Vector2(self.screen_width / 2, self.screen_height / 2)

        self.focus = None
        self.speed = speed
        self.acc = acc
        self.drag = drag
        self.shift = pg.math.Vector2(0, 0)
        self.vel = pg.math.Vector2(0, 0)

        self.shake_start = 0
        self.shake_duration = 0
        self.shake_magnitude = 0

        self.drag_rect = None

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
            self.shift += shift

    def update(self, dt, t):
        if self.focus == None:
            return

        needed_shift = self.shift
        focus_screen_rect = self.shifted_rect(self.focus.rect)
        self.drag_rect = pg.Rect(0, 0, self.drag * 2, self.drag * 2)
        self.drag_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.drag_rect.center -= (self.focus.vel * dt) * 3
        
        difference = pg.math.Vector2(self.focus.rect.center) - self.drag_rect.center

        if not self.drag_rect.colliderect(focus_screen_rect):
            needed_shift = needed_shift.lerp(difference, 0.05)


        fat_focus = pg.Rect(self.focus.rect)
        fat_focus.width = self.scene.screen_rect.width
        fat_focus.center = self.focus.rect.center

        rect = pg.Rect(self.scene.screen_rect)
        rect.left = self.shift.x
        rect.top = self.shift.y

        rect.left = needed_shift.x
        for edge in self.scene.edges:
            if rect.colliderect(edge.rect):
                to_the_right = edge.rect.left >= self.focus.rect.right
                to_the_left = edge.rect.right <= self.focus.rect.left
                in_y_range = fat_focus.colliderect(edge.rect)
                if to_the_right and in_y_range:
                    rect.right = edge.rect.left
                elif to_the_left and in_y_range:
                    rect.left = edge.rect.right
        needed_shift.x = rect.x

        self.shift = needed_shift

        self.handle_screenshake(t)