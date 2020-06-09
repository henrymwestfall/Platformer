import math

import pygame as pg

from .foundation import RigidBody
from colors import *

class HitBox(RigidBody):
    def __init__(self, parent, x, y, width, height, birth, lifetime, power, knockback, stick=True, color=None):
        super().__init__(parent.scene)

        self.parent = parent

        self.birth = birth
        self.lifetime = lifetime # seconds it will last
        self.power = power # how much damage it does
        self.knockback = knockback # how far it knocks back enemies
        
        self.image = pg.Surface([width, height])
        if color != None:
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.stick = stick
        self.relative_position = pg.math.Vector2(self.rect.center) - pg.math.Vector2(self.parent.rect.center)

    def update(self, dt, t):
        super().update(dt, t)

        # stick if necessary
        if self.stick:
            parent_pos = pg.math.Vector2(self.parent.rect.center)
            relative_position = pg.math.Vector2(self.rect.center) - parent_pos
            if relative_position != self.relative_position:
                self.rect.center = parent_pos + self.relative_position
        
        # get colliding rigid bodies
        collisions = pg.sprite.spritecollide(self, self.scene.rigid_bodies, False)
        for sprite in collisions:
            if isinstance(sprite, HitBox) or (sprite is self.parent):
                continue

            
            # deal damage and apply knockback
            if hasattr(sprite, "health"):
                if type(sprite) != type(self.parent):
                    sprite.health -= self.power

                diff = pg.math.Vector2(sprite.rect.center) - pg.math.Vector2(self.parent.rect.center)
                if diff.length() == 0:
                    diff.x += 1
                diff = diff.normalize()
                knockback_vector = diff * (self.knockback) + self.parent.vel + pg.math.Vector2(0, -400)

                sprite.vel = knockback_vector

        # determine if we should die
        if t - self.birth >= self.lifetime:
            self.kill()
            del self