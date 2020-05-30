import pygame as pg

class RigidBody(pg.sprite.DirtySprite):
    def __init__(self, scene):
        pg.sprite.DirtySprite.__init__(self, scene.children, scene.rigid_bodies)

        self.scene = scene

        # groups that this checks for collisions with
        self.collision_groups = [
            self.scene.rigid_bodies,
            self.scene.static_bodies,
            self.scene.projectiles
        ]

        # movement attributes
        self.vel = pg.math.Vector2(0, 0)
        self.landed = False
        self.was_landed_last_frame = False
        self.underneath = None

    def update(self, dt, t):
        # move down from gravity

        # check for static body collisions
        self.landed = False
        for sprite in self.scene.static_bodies:
            if pg.sprite.collide_rect(self, sprite):
                # if we landed on it
                if (self.vel.y >= 0) and (self.rect.centerx in range(sprite.rect.left, sprite.rect.right)):
                    self.rect.bottom = sprite.rect.top
                    self.vel.y = 0
                    self.landed = True
                    self.underneath = sprite
                
                # head butted it
                elif (self.vel.y < 0) and (self.rect.centerx in range(sprite.rect.left, sprite.rect.right)):
                    self.rect.top = sprite.rect.bottom
                    self.vel.y = 0
                
        if not self.landed:
             self.vel = self.vel.lerp(self.scene.terminal_velocity, self.scene.gravity)

        

class StaticBody(pg.sprite.DirtySprite):
    def __init__(self, scene):
        pg.sprite.DirtySprite.__init__(self, scene.children, scene.static_bodies)

        self.scene = scene

        self.collision_groups = []

    def update(self, dt, t):
        pass

# TODO: particle and projectile class
class Particle(pg.sprite.DirtySprite):
    def __init__(self, scene):
        pg.sprite.DirtySprite.__init__(self, scene.children, scene.particles)

        self.scene = scene
        self.collision_groups = []

        self.life_time = 0

    def update(self, dt, t):
        pass
