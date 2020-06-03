import sys

import pygame as pg

from scenes.test_scene import Demo

class Game:
    def __init__(self):
        # scene info
        self.scenes = []
        self.scenes_by_name = {}
        self.current_scene = None

        self.clock = None
        self.time = 0

        # screen settings
        self.screen = None
        self.screen_resolution = (900, 600)

    def start(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_resolution)
        self.clock = pg.time.Clock()
        self.time = 0

        self.current_scene = Demo(self)
        self.current_scene.start()

        self.main_loop()

    def main_loop(self):
        done = False
        while not done:
            dt = self.clock.tick(60) / 1000.0
            self.time += dt
            if self.current_scene == None:
                continue

            self.current_scene.handle_events()

            if self.current_scene.keys_pressed[pg.K_q]:
                done = True

            self.current_scene.update(dt, self.time)
            self.current_scene.draw()

            pg.display.flip()
        self.quit()

    def quit(self):
        pg.quit()
        sys.exit()
