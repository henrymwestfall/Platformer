import pygame as pg

class Trigger(pg.sprite.DirtySprite):
    def __init__(self, scene, x, y, width, height, foci, callback):
        self.scene = scene
        self.rect = pg.Rect(x, y, width, height)
        self.foci = foci
        self.callback = callback
    
    def update(self, dt, t):
        for focus in self.foci:
            if self.rect.colliderect(focus.rect):
                self.callback()