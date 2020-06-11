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
from sprites.score_tracker import ScoreTracker


class SaltedReef(Scene):
    def __init__(self, game):
        super().__init__("Salted Reef", game)

        self.player = None

        raw_map = load_tile_map("SaltedReef")
        self.express_map(raw_map)

        self.background = BLACK

        ScoreTracker(self, 0, 0)

    def start(self):
        pg.display.set_caption("Combat Test")

        self.player = Player(self, self.screen.get_width() // 2, 600)
        self.camera.set_focus(self.player)

        for edge in self.edges:
            edge.player = self.player
        for sprite in self.rigid_bodies:
            if isinstance(sprite, Mob):
                sprite.set_target(self.player)

    def update(self, dt, t):
        super().update(dt, t)