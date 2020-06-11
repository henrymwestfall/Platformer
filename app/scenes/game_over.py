import pygame as pg

from scene import Scene
from colors import RED, BLACK
from sprites.foundation import StaticBody

class GameOver(Scene):
    def __init__(self, game):
        super().__init__("Game Over", game)
        self.background = BLACK

        font = pg.font.Font(pg.font.get_default_font(), 64)
        self.go_image = font.render("Game Over", True, RED)
        self.go_rect = self.go_image.get_rect()
        self.go_rect.center = self.screen_rect.center

        font = pg.font.Font(pg.font.get_default_font(), 16)
        self.cont_image = font.render("press any key to restart", True, RED)
        self.cont_rect = self.cont_image.get_rect()
        self.cont_rect.midtop = self.go_rect.midbottom

        self.origin = None

    def start(self, origin):
        self.origin = origin

    def draw(self):
        self.screen.fill(self.background)
        self.screen.blit(self.go_image, self.go_rect)
        self.screen.blit(self.cont_image, self.cont_rect)

        for event in self.events:
            if event.type == pg.KEYDOWN:
                self.game.set_screen(self, self.origin)