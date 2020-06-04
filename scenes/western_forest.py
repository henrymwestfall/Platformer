import random
import time
import os
import pickle

import pygame as pg
import numpy as np

from scene import Scene
from sprites.test import Platform, Player, Coin, ScoreTracker

class WesternForest(Scene):
    def __init__(self, game):
        super().__init__("Western Forest", game)

        self.player = None
        self.camera_focus = self.player

        path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "maps", "Western Forest.pkl")
        with open(path, "rb") as f:
            raw_map = pickle.load(f)
            for x, line in enumerate(raw_map):
                for y, cell in enumerate(line):
                    if int(cell) == 1:
                        Platform(self, x * 64, y * 64, 64, 64)
                    elif int(cell) == 2:
                        Coin(self, x * 64, y * 64)
        ScoreTracker(self, 0, 0)

        self.kill_depth = 1000
                            

    def start(self):
        pg.display.set_caption("Demo")

        self.player = Player(self, 1000, 500)
        self.camera_focus = self.player

        self.kill_depth = max([p.rect.bottom for p in self.static_bodies]) + 200
        print(self.kill_depth)

    def update(self, dt, t):
        super().update(dt, t)
        if self.player.rect.top >= self.kill_depth:
            self.__init__(self.game)
            self.start()