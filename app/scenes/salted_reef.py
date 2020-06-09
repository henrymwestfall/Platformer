import os
import pickle
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import pygame as pg

from colors import *
from scene import Scene, load_tile_map
from sprites.platform import Platform
from sprites.player import Player
from sprites.mob import Mob


class SaltedReef(Scene):
    def __init__(self, game):
        super().__init__("Salted Reef", game)

        self.player = None

        raw_map = load_tile_map("room2")
        self.express_map(raw_map)

    def start(self):
        pg.display.set_caption("Combat Test")

        self.player = Player(self, self.screen.get_width() // 2, 300)
        self.camera.set_focus(self.player)

        for edge in self.edges:
            edge.player = self.player

    def update(self, dt, t):
        super().update(dt, t)