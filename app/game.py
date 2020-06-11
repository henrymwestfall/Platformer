import sys

import pygame as pg

from scenes.test_scene import Demo
from scenes.western_forest import WesternForest
from scenes.combat_test import CombatTest
from scenes.salted_reef import SaltedReef
from scenes.game_over import GameOver

class Game:
    def __init__(self):
        # scene info
        self.scenes_by_name = {}
        self.current_scene = None

        self.clock = None
        self.time = 0

        # screen settings
        self.screen = None
        self.screen_resolution = (900, 600)

    def set_screen(self, origin, scene):
        if scene in self.scenes_by_name:
            self.current_scene = self.scenes_by_name[scene]
            self.current_scene.start(origin)
        elif scene in self.scenes_by_name.values():
            self.current_scene = scene
            scene.start(origin)
        else:
            origin.start(origin)

    def start(self):
        print("starting game")
        pg.init()
        self.screen = pg.display.set_mode(self.screen_resolution)
        self.clock = pg.time.Clock()
        self.time = 0

        self.current_scene = SaltedReef(self)
        self.current_scene.start(None)

        GameOver(self)

        self.main_loop()

    def main_loop(self):
        done = False
        print("starting mainloop")
        while not done:
            dt = self.clock.tick(60) / 1000.0
            self.time += dt
            if self.current_scene == None:
                continue

            self.current_scene.handle_events()

            if not pg.mouse.get_focused():
                continue

            if self.current_scene.keys_pressed[pg.K_q]:
                done = True

            self.current_scene.update(dt, self.time)
            self.current_scene.draw()

            pg.display.flip()
        self.quit()

    def quit(self):
        pg.quit()
        sys.exit()
