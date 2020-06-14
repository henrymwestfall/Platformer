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
from sprites.platform import Platform
from sprites.edge import Edge
from sprites.mob import Mob
from sprites.collectables import Coin

def load_tile_map(name, *subdirs):
    if ".pkl" in name:
        file_name = name
    else:
        file_name = name + ".map"
    path = os.path.join(*subdirs, "maps")
    text = pkg_resources.read_binary(path, file_name)
    raw_data = pickle.loads(text)
    return raw_data

class Scene:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.game.scenes_by_name[self.name] = self

        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.drawing = True

        # groups / collision layers
        self.children = pg.sprite.Group() # all child sprites

        self.rigid_bodies = pg.sprite.Group() # affected by gravity
        self.hitboxes = pg.sprite.Group()
        self.static_bodies = pg.sprite.Group() # immobile platforms
        self.projectiles = pg.sprite.Group() # unaffected by gravity
        self.particles = pg.sprite.Group() # unaffected by anything
        self.hud = pg.sprite.Group()
        self.triggers = pg.sprite.Group() # not drawn
        self.edges = pg.sprite.Group()

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
        self.camera = Camera(self, 1000, 0.05, 300)

        self.platform_columns = []


    def express_map(self, tile_map, tile_size=64):
        for x in range(len(tile_map)):
            self.platform_columns.append(pg.sprite.Group())

        for x, line in enumerate(tile_map):
            platform_y_start = None
            last_was_platform = False
            for y, cell in enumerate(line):
                if int(cell) == 1 and not last_was_platform:
                    last_was_platform = True
                    platform_y_start = y
                elif int(cell) == 2:
                    Coin(self, x * tile_size, y * tile_size)
                elif int(cell) == 3:
                    Edge(self, x * tile_size, y * tile_size, tile_size, tile_size)
                elif int(cell) == 4:
                    Mob(self, x * tile_size, y * tile_size)

                if last_was_platform and (int(cell) != 1):
                    x_pxl = x * tile_size
                    y_pxl = platform_y_start * tile_size
                    height = (y - platform_y_start) * tile_size
                    width = tile_size
                    p = Platform(self, x_pxl, y_pxl, width, height)
                    self.platform_columns[x].add(p)

                    if x > 0:
                        self.platform_columns[x - 1].add(p)
                    if x < len(self.platform_columns) - 1:
                        self.platform_columns[x + 1].add(p)

                    last_was_platform = False

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
        if self.drawing:
            self.screen.fill(self.background)

            # order is important
            self.draw_group(self.static_bodies)
            self.draw_group(self.projectiles)
            self.draw_group(self.rigid_bodies)
            self.draw_group(self.hitboxes)
            self.draw_group(self.particles)
            self.draw_group(self.hud)
            self.draw_group(self.edges)

            for line in self.camera.debug_lines:
                pg.draw.line(self.screen, *line)

        else:
            self.screen.fill(BLACK)

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
        synth_dt = dt
        self.camera.update(synth_dt, t)

        for edge in self.edges:
            edge.update(synth_dt, t)
        if any([self.camera.shifted_rect(edge.rect).colliderect(self.screen_rect) for edge in self.edges]):
            self.drawing = False
        else:
            self.drawing = True

        for hitbox in self.hitboxes:
            hitbox.update(synth_dt, t)
        for sprite in self.rigid_bodies:
            sprite.update(synth_dt, t)
        for particle in self.particles:
            particle.update(synth_dt, t)
        for hud_e in self.hud:
            hud_e.update(synth_dt, t)
        for trigger in self.triggers:
            trigger.update(synth_dt, t)

    def close(self):
        pass


class Area(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        self.scenes = []
        path = os.path.join(os.path.dirname(__file__), "maps", self.name)
        for i, map_file in enumerate(os.listdir(path)):
            s = Scene(f"{self.name}-{i + 1}", self.game)

            map_data = load_tile_map(map_file, self.name)
            s.express_map(map_data)

            self.scenes.append(s)
        
