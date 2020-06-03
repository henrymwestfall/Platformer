import pygame as pg

from scene import Scene
from sprites.test import Platform, Player

import random
import time

class Demo(Scene):
    def __init__(self, game):
        Scene.__init__(self, "Test", game)

        self.widths = range(30, 150)
        self.y_range = range(30, 570)
        self.gaps = range(50, 150)

        self.player = None
        self.camera_focus = self.player

    def start(self):
        pg.display.set_caption("Demo")
        for i in range(10):
            Platform(self, i * 2000 + 550, 350, 2000, 32)
        Platform(self, 400, 200, 32, 100)
        Platform(self, 500, 200, 32, 100)
        
        a = Platform(self, 400, 100, 32, 32)
        b = Platform(self, 400, 132, 32, 32)
        print(a.compress_with(b, True, True))

        self.player = Player(self, 450, 100)
        self.camera_focus = self.player

    def handle_events(self):
        super().handle_events()
        

    def update(self, dt, t):
        super().update(dt, t)

        to_the_right = 0
        for platform in self.static_bodies:
            if platform.rect.x >= self.player.rect.x:
                to_the_right += 1
            if self.player.rect.x - platform.rect.x >= 10000:
                platform.kill()
                del platform

        if to_the_right < 20:
            last_x = self.game.screen.get_width() + self.camera_shift.x
            last_y = self.game.screen.get_height() / 2 + self.camera_shift.y
            last_width = min(self.widths)
            for i in range(8):
                width = random.choice(self.widths)
                x = last_x + width / 2 + last_width / 2 + random.choice(self.gaps)
                y = last_y * (random.randint(50, 110) / 100)
                if int(y) not in self.y_range:
                    y = self.game.screen.get_height() / 2 + self.camera_shift.y
                platform = Platform(self, x, int(y), width, width)
                last_x = x
                last_y = y
                last_width = width

        if self.player.rect.y > self.game.screen.get_height() + 200:
            self.close()

    def close(self):
        self.__init__(self.game)
        self.start()
