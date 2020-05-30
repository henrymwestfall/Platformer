import pygame as pg

from scene import Scene
from sprites.test import TestStaticBody, TestRigidBody

import random

class TestScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, "Test", game)

        self.widths = range(100, 300)
        self.y_range = range(30, 570)
        self.gaps = range(50, 150)

        self.player = None
        self.camera_focus = self.player

    def start(self):
        TestStaticBody(self, 450, 300, 900)
        self.player = TestRigidBody(self, 450, 100)
        self.camera_focus = self.player

    def handle_events(self):
        super().handle_events()

        # TODO: define in player class
        for e in self.events:
            if e.type == pg.USEREVENT:
                pg.time.set_timer(pg.USEREVENT, 0)
                if self.keys_pressed[pg.K_UP]:
                    self.player.vel += pg.math.Vector2(0, -600)
                self.player.long_jump_timer_started = False
                break

    def update(self, dt, t):
        super().update(dt, t)

        to_the_right = 0
        for platform in self.static_bodies:
            if self.player.underneath == platform or platform.rect.x > self.player.rect.x:
                to_the_right += 1
            if self.player.rect.x - platform.rect.x >= 2000:
                platform.kill()
                del platform

        if to_the_right < 4:
            last_x = self.game.screen.get_width() + self.camera_shift.x
            last_y = self.game.screen.get_height() / 2 + self.camera_shift.y
            last_width = min(self.widths)
            for i in range(8):
                width = random.choice(self.widths)
                x = last_x + width / 2 + last_width / 2 + random.choice(self.gaps)
                y = last_y * (random.randint(50, 110) / 100)
                if int(y) not in self.y_range:
                    y = self.game.screen.get_height() / 2 + self.camera_shift.y
                platform = TestStaticBody(self, x, int(y), width)
                last_x = x
                last_y = y
                last_width = width

        if self.player.rect.y > self.game.screen.get_height() + 200:
            self.close()

    def close(self):
        self.__init__(self.game)
        self.start()
