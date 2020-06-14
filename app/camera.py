import random
import math

import pygame as pg

from colors import *

class Camera:
    def __init__(self, scene, speed, acc, drag):
        self.scene = scene
        self.screen = self.scene.screen
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.screen_middle = pg.math.Vector2(self.screen_width / 2, self.screen_height / 2)

        self.focus = None
        self.focus_offset = pg.math.Vector2(0, 0)
        self.speed = speed
        self.acc = acc
        self.drag = drag
        self.shift = pg.math.Vector2(0, 0)
        self.vel = pg.math.Vector2(0, 0)

        self.shake_start = 0
        self.shake_duration = 0
        self.shake_magnitude = 0

        self.drag_rect = None

        self.debug_lines = []
        self.last_shift_amount = pg.math.Vector2(0, 0)
        self.debugging = False

    def set_focus(self, new_focus):
        self.focus_offset.x = -100
        self.focus = new_focus

    def enable_debugging(self):
        self.debugging = True

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

        self.drag_rect = pg.Rect(0, 0, self.drag, self.drag)

        self.focus_screen_rect = self.shifted_rect(self.focus.rect)

        inner_line_x = 75
        outer_line_x = 150

        self.debug_lines = []

        # detect collisions with inner and outer lines
        if self.focus.vel.x > 0 and self.focus_screen_rect.right >= self.screen_middle.x + outer_line_x:
            self.focus_offset.x = -inner_line_x - self.focus_screen_rect.width * 0.5
        elif self.focus.vel.x > 0 and self.focus_screen_rect.right >= self.screen_middle.x - inner_line_x and self.focus_screen_rect.right <= self.screen_middle.x:
            self.focus_offset.x = -inner_line_x - self.focus_screen_rect.width * 0.5

        if self.focus.vel.x < 0 and self.focus_screen_rect.left <= self.screen_middle.x - outer_line_x:
            self.focus_offset.x = inner_line_x + self.focus_screen_rect.width
        elif self.focus.vel.x < 0 and self.focus_screen_rect.left <= self.screen_middle.x + inner_line_x and self.focus_screen_rect.left >= self.screen_middle.x:
            self.focus_offset.x = inner_line_x + self.focus_screen_rect.width

        self.focus_offset.y = 0

        # add debug lines
        if self.debugging:
            color_map = [RED, RED, FOREST_GREEN, FOREST_GREEN, WHITE]
            for i, debug_line_offset in enumerate([-outer_line_x, outer_line_x, -inner_line_x, inner_line_x, self.focus_offset.x]):
                start = (self.screen_middle.x + debug_line_offset, 0)
                end = (self.screen_middle.x + debug_line_offset, self.screen_height)
                self.debug_lines.append((color_map[i], start, end))
            
        # calculate difference from the center of the screen
        difference = self.focus_screen_rect.center - (self.screen_middle + self.focus_offset)
        
        # disable shifting if focus point and focus entity are in the same inner-outer region
        need_shift = True
        if (self.focus_screen_rect.centerx < self.screen_middle.x + outer_line_x and self.focus_screen_rect.centerx > self.screen_middle.x + inner_line_x
                and self.focus_offset.x < self.screen_middle.x + outer_line_x and self.focus_offset.x > self.screen_middle.x + inner_line_x):
            need_shift = False
        elif (self.focus_screen_rect.centerx < self.screen_middle.x - inner_line_x and self.focus_screen_rect.centerx > self.screen_middle.x - outer_line_x
                and self.focus_offset.x < self.screen_middle.x + outer_line_x and self.focus_offset.x > self.screen_middle.x + inner_line_x):
            need_shift = False
        if math.copysign(1, self.last_shift_amount.x) != math.copysign(1, self.focus.vel.x):
            need_shift = True

        # add to needed_shift if necessary
        if need_shift:
            vel = difference / 32
            if vel.x > self.focus.vel.x * 2:
                self.last_shift_amount = vel
                needed_shift += self.last_shift_amount
            else:
                self.last_shift_amount = vel * 3
                needed_shift += self.last_shift_amount


        fat_focus = pg.Rect(self.focus.rect)
        fat_focus.width = self.scene.screen_rect.width * 2
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

        tall_focus = pg.Rect(self.focus.rect)
        tall_focus.height = self.screen_height * 2
        tall_focus.center = self.focus.rect.center

        rect.top = needed_shift.y
        for edge in self.scene.edges:
            if rect.colliderect(edge.rect):
                below = edge.rect.top >= self.focus.rect.bottom
                above = edge.rect.bottom <= self.focus.rect.top
                in_x_range = tall_focus.colliderect(edge.rect)
                if below and in_x_range:
                    rect.bottom = edge.rect.top
                elif above and in_x_range:
                    rect.top = edge.rect.bottom
        needed_shift.y = rect.y

        self.shift = needed_shift

        self.handle_screenshake(t)