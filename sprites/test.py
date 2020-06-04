import math

import pygame as pg

from .foundation import RigidBody, StaticBody, Particle
from colors import *

class Platform(StaticBody):
    def __init__(self, scene, x, y, width, height):
        StaticBody.__init__(self, scene)

        self.image = pg.Surface([width, height])
        self.image.fill(FOREST_GREEN)
        internal_image = pg.Surface([width - 8, height - 8])
        internal_image.fill(FOREST_GREEN)
        rect = pg.Rect(4, 4, width - 4, height - 4)
        self.image.blit(internal_image, rect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.friction = 100

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


class Player(RigidBody):
    def __init__(self, scene, x, y):
        RigidBody.__init__(self, scene)

        self.image = pg.Surface([32, 52])
        self.image.fill(BLUE)
        internal_image = pg.Surface([24, 24])
        internal_image.fill(RED)
        rect = pg.Rect(4, 4, 28, 28)
        self.image.blit(internal_image, rect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.speed = 600
        self.acc = 0.1

        self.jump_strength = 1000
        self.jump_cut = 0.5

        self.climb = 250

    def update(self, dt, t):
        landed = len(self.collisions["down"]) > 0
        touching_left = len(self.collisions["left"]) > 0
        touching_right = len(self.collisions["right"]) > 0

        # apply gravity
        if not landed:
            self.vel += pg.math.Vector2(0, self.scene.gravity) * dt

        # jump
        if landed and self.scene.keys_pressed[pg.K_UP]:
            self.vel.y = -self.jump_strength
        elif self.vel.y < 0 and not self.scene.keys_pressed[pg.K_UP]:
            self.vel.y *= self.jump_cut

        # handle climbing
        
        if not landed and (touching_left or touching_right):
            self.vel.y = 0
            if self.scene.keys_pressed[pg.K_UP]:
                self.vel.y = -self.climb
            elif self.scene.keys_pressed[pg.K_DOWN]:
                self.vel.y = self.climb
        
        # move left/right
        self.moving = False

        if self.scene.keys_pressed[pg.K_RIGHT] ^ self.scene.keys_pressed[pg.K_LEFT]:
            if self.scene.keys_pressed[pg.K_RIGHT]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(self.speed, 0), self.acc).x
                self.moving = True
            elif self.scene.keys_pressed[pg.K_LEFT]:
                self.vel.x = self.vel.lerp(pg.math.Vector2(-self.speed, 0), self.acc).x
                self.moving = True
        else:
            self.vel.x = 0

        if landed and not self.moving:
            friction = self.collisions["down"][0].friction * math.copysign(1, -self.vel.x)
            new_vel_x = self.vel.x + friction
            if math.copysign(1, self.vel.x) == math.copysign(1, new_vel_x):
                self.vel.x = new_vel_x
            else:
                self.vel.x = 0

        self.image = pg.Surface([self.rect.width, self.rect.height])
        self.image.fill(SKY_BLUE)
        """
        internal_image = pg.Surface([24, 24])
        if self.moving:
            internal_image.fill(RED)
        else:
            internal_image.fill(BLUE)
        rect = pg.Rect(4, 4, 28, 28)
        self.image.blit(internal_image, rect)"""

        if self.scene.keys_pressed[pg.K_SPACE]:
            self.scene.shake_screen(t, 50, 2)
        
        # update position
        self.move(dt)
        rect_pos = pg.math.Vector2(self.pos)
        if rect_pos.x < 0:
            rect_pos.x = math.ceil(rect_pos.x)
        elif rect_pos.x > 0:
            rect_pos.x = math.floor(rect_pos.x)
        self.rect.topleft = rect_pos


class TestParticle(Particle):
    def __init__(self, scene, center, push_vector):
        Particle.__init__(self, scene)

        self.vel = push_vector
        self.radius = 4

        self.image = pg.Surface([self.radius * 2, self.radius * 2])
        pg.draw.circle(self.image, WHITE, center, self.radius)
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.life_time = 1
        self.life = self.life_time

    def update(self, dt, t):
        center = pg.math.Vector2(self.rect.center) + self.vel
        
        #color = pg.Color(255, 255, 255, int(255 * (self.life / self.life_time)))
        radius = int(self.radius * self.life / self.life_time)
        self.image = pg.Surface([radius * 2, radius * 2])
        pg.draw.circle(self.image, WHITE, self.rect.center, radius)
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.life -= dt
        if self.life < 0:
            self.kill()
        