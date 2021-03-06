import pygame as pg

class RigidBody(pg.sprite.DirtySprite):
    def __init__(self, scene):
        super().__init__(scene.children, scene.rigid_bodies)

        self.scene = scene

        # groups that this checks for collisions with
        self.collision_groups = [
            self.scene.rigid_bodies,
            self.scene.static_bodies,
            self.scene.projectiles
        ]

        # movement attributes
        self.vel = pg.math.Vector2(0, 0)
        self.collisions = {"up": [], "down": [], "left": [], "right": []}

        self.landed = False
        self.touching_left = False
        self.touching_right = False
        self.climbing = False
        self.being_knocked_back = False
        self.knockback_time = 0

    def update(self, dt, t):
        # update collision variables
        self.landed = len(self.collisions["down"]) > 0
        self.touching_left = len(self.collisions["left"]) > 0
        self.touching_right = len(self.collisions["right"]) > 0

    def apply_gravity(self, dt):
        if not self.landed:
            self.vel += pg.math.Vector2(0, self.scene.gravity) * dt

    def move(self, dt):
        self.collisions = {"up": [], "down": [], "left": [], "right": []}

        self.pos.x += self.vel.x * dt
        self.rect.left = self.pos.x
        
        # check collisions with static bodies while moving along the x-axis
        try:
            hit_list = pg.sprite.spritecollide(self, self.scene.platform_columns[self.rect.left // 64], False)
        except IndexError as e:
            hit_list = pg.sprite.spritecollide(self, self.scene.static_bodies, False)
        for static_body in hit_list:
            if (self.vel.x < 0) and (self.rect.right > static_body.rect.right): # moving left
                self.rect.left = static_body.rect.right
                self.pos.x = self.rect.left
                self.collisions["left"].append(static_body)
                self.vel.x = 0
            elif (self.vel.x > 0) and (self.rect.left < static_body.rect.left): # moving right
                self.rect.right = static_body.rect.left
                self.pos.x = self.rect.left
                self.collisions["right"].append(static_body)
                self.vel.x = 0

        # check collisions with edges while moving along the x-axis
        hit_list = pg.sprite.spritecollide(self, self.scene.edges, False)
        for edge in hit_list:
            if (self.vel.x > 0) and (self.rect.right < edge.rect.right): # moving right
                self.rect.left = edge.rect.right
                self.pos.x = self.rect.left
            elif (self.vel.x < 0) and (self.rect.left > edge.rect.left): # moving left
                self.rect.right = edge.rect.left
                self.pos.x = self.rect.left
        
        self.pos.y += self.vel.y * dt
        self.rect.top = self.pos.y

        # check for collisions with static bodies while moving in the y-axis
        try:
            hit_list = pg.sprite.spritecollide(self, self.scene.platform_columns[self.rect.left // 64], False)
        except IndexError as e:
            hit_list = pg.sprite.spritecollide(self, self.scene.static_bodies, False)
        self.landed = False
        self.underneath = None
        for static_body in hit_list:
            if self.vel.y < 0: # moving up
                self.rect.top = static_body.rect.bottom
                self.pos.y = self.rect.top
                self.vel.y = 0
                self.collisions["up"].append(static_body)
            elif self.vel.y > 0: # moving down
                self.rect.bottom = static_body.rect.top
                self.pos.y = self.rect.top
                self.vel.y = 0
                self.collisions["down"].append(static_body)

        # check for collisions with edges while moving in the y-axis
        hit_list = pg.sprite.spritecollide(self, self.scene.edges, False)
        self.landed = False
        self.underneath = None
        for edge in hit_list:
            if self.vel.y > 0: # moving down
                self.rect.top = edge.rect.bottom
                self.pos.y = self.rect.top
            elif self.vel.y < 0: # moving up
                self.rect.bottom = edge.rect.top
                self.pos.y = self.rect.top
        

class StaticBody(pg.sprite.DirtySprite):
    def __init__(self, scene):
        super().__init__(scene.children, scene.static_bodies)

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
