import os
import pickle
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import pygame as pg

from colors import *
from scene import Scene
from sprites.platform import Platform
from sprites.player import Player
from sprites.mob import Mob


class CombatTest(Scene):
    def __init__(self, game):
        super().__init__("Combat Test", game)

        self.player = None

        self.tile_size = 64
        path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "maps", "CombatTest.pkl")
        text = pkg_resources.read_binary("maps", "CombatTest.pkl")
        raw_map = pickle.loads(text)
        for x, line in enumerate(raw_map):
            for y, cell in enumerate(line):
                if int(cell) == 1:
                    Platform(self, x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
        

    def start(self):
        pg.display.set_caption("Combat Test")

        self.player = Player(self, self.screen.get_width() // 2, 300)
        m = Mob(self, 2 * self.screen.get_width() // 3, 300)
        m.set_target(self.player)
        self.camera.set_focus(self.player)

    def update(self, dt, t):
        super().update(dt, t)

        for body in self.rigid_bodies:
            if isinstance(body, Mob):
                break
        else:
            m = Mob(self, 2 * self.screen.get_width() // 3, 300)
            m.set_target(self.player)