import pickle

import pygame as pg

from scene import Scene, load_tile_map
from camera import Camera
from colors import *
from sprites.platform import Platform
from sprites.edge import Edge
from sprites.player import Player
from sprites.mob import Mob
from sprites.foundation import RigidBody


class PointBody(RigidBody):
    def __init__(self, scene):
        super().__init__(scene)

        self.image = pg.Surface([2, 2])
        self.rect = self.image.get_rect()

    def snap_to(self, position):
        self.rect.center = position

class LevelEditor(Scene):
    def __init__(self):
        self.map_height = 64
        self.map_width = 128
        self.tile_size = 16
        self.save_file = "LE2.map"

        # load map if it exists
        if not os.path.exists(f"{self.save_file}.map"):
            self.current_map = [[None for y in range(self.map_height)] for x in range(self.map_width)]
        else:
            with open(f"{self.save_file}.map", "rb") as f:
                self.current_map = pickle.load(f)

        self.map_surface = pg.Surface([self.tile_size * self.map_width, self.tile_size * self.map_height])
        self.map_surface.fill(SKY_BLUE)

        self.pointer = PointBody(self)
        self.camera.set_focus(self.pointer)

        self.input_map = {
            "1": Platform,
            "2": Edge,
            "3": Mob
        }

    def save(self):
        pass
    
    def update(self, dt, t):
        pass


        