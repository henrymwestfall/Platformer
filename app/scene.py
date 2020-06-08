import random
import os
import pickle
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import pygame as pg

from colors import *
from camera import Camera

def load_tile_map(name):
    if ".pkl" in name:
        file_name = name
    else:
        file_name = name + ".pkl"
    text = pkg_resources.read_binary("maps", file_name)
    raw_data = pickle.loads(text)
    return raw_data

class Scene:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.game.scenes_by_name[self.name] = self

        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()

        # groups / collision layers
        self.children = pg.sprite.Group() # all child sprites

        self.rigid_bodies = pg.sprite.Group() # affected by gravity
        self.static_bodies = pg.sprite.Group() # immobile platforms
        self.projectiles = pg.sprite.Group() # unaffected by gravity
        self.particles = pg.sprite.Group() # unaffected by anything
        self.hud = pg.sprite.Group()

        # environment
        self.background = BLACK
        self.gravity = 3000
        self.terminal_velocity = pg.math.Vector2(0, 1250)

        # input
        self.events = []
        self.keys_pressed = []
        self.__mouse_pos = pg.math.Vector2(0, 0)
        self.mouse_state = (False, False, False)

        # camera
        self.camera = Camera(self, 500, 0.04, 25)

    def get_relative_mouse_pos(self):
        return self.__mouse_pos + self.camera.shift

    def get_window_mouse_pos(self):
        return self.__mouse_pos
    
    def handle_events(self):
        self.events = pg.event.get()
        self.keys_pressed = pg.key.get_pressed()
        self.__mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
        self.mouse_state = pg.mouse.get_pressed()

    def draw(self):
        self.screen.fill(self.background)
        
        # order matters
        self.draw_group(self.static_bodies)
        self.draw_group(self.projectiles)
        self.draw_group(self.rigid_bodies)
        self.draw_group(self.particles)
        self.draw_group(self.hud)

    def draw_group(self, group):
        for e in group:
            if group == self.hud:
                rect = e.rect
            else:
                rect = self.camera.shifted_rect(e.rect)
            
            if rect.colliderect(self.screen_rect):
                self.screen.blit(e.image, rect)
                
    def start(self):
        pass

    def update(self, dt, t):
        self.camera.update(dt, t)

        for sprite in self.rigid_bodies:
            sprite.update(dt, t)
        for particle in self.particles:
            particle.update(dt, t)
        for hud_e in self.hud:
            hud_e.update(dt, t)

    def close(self):
        pass


class Area(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

