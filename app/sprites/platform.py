import random

import pygame as pg

from colors import *
from .foundation import StaticBody


class Platform(StaticBody):
    def __init__(self, scene, x, y, width, height):
        StaticBody.__init__(self, scene)

        try:
            self.image = pg.Surface([width, height])
        except Exception as e:
            print(width, height)
            raise e
        self.image.fill(BLUE)
        pg.draw.line(self.image, WHITE, (0, 0), (width, 0), 5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.friction = 75

    def compress_with(self, other, kill=False, delete=False):
        # make sure they align to form a valid rectangle

        expanded = self.rect
        expanded.width += 2
        expanded.height += 2
        expanded.left -= 1
        expanded.right += 1
        expanded.top -= 1
        expanded.bottom += 1

        other_expanded = other.rect
        other_expanded.width += 2
        other_expanded.height += 2
        other_expanded.left -= 1
        other_expanded.right += 1
        other_expanded.top -= 1
        other_expanded.bottom += 1
        
        if not expanded.colliderect(other):
            return [self, other]

        if (self.rect.left == other.rect.left) and (self.rect.width == other.rect.width):
            height = max([self.rect.bottom, other.rect.bottom]) - min([self.rect.top, other.rect.top])
            y = min([self.rect.top, other.rect.top])
            x = self.rect.x
            width = self.rect.width
        elif (self.rect.top == other.rect.top) and (self.rect.height == other.rect.height):
            width = max([self.rect.right, other.rect.right]) - min([self.rect.left, other.rect.left])
            x = min([self.rect.left, other.rect.left])
            y = self.rect.y
            height = self.rect.height
        else:
            return [self, other]
        
        new_platform = Platform(self.scene, x, y, width, height)
        
        if kill:
            self.kill()
            other.kill()
            if delete:
                del other
                del self
            
        return [new_platform]