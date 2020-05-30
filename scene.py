import pygame as pg

from colors import SKY_BLUE, BLACK

class Scene:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.game.scenes_by_name[self.name] = self

        # groups / collision layers
        self.children = pg.sprite.Group() # all child sprites

        self.rigid_bodies = pg.sprite.Group() # affected by gravity
        self.static_bodies = pg.sprite.Group() # immobile platforms
        self.projectiles = pg.sprite.Group() # unaffected by gravity
        self.particles = pg.sprite.Group() # unaffected by anything

        # environment
        self.background = SKY_BLUE
        self.gravity = 0.05
        self.terminal_velocity = pg.math.Vector2(0, 800)

        # input
        self.events = []
        self.keys_pressed = []

        # camera
        self.camera_focus = None
        self.camera_speed = 300
        self.camera_acc = 0.025
        self.camera_drag = 100
        self.camera_shift = pg.math.Vector2(0, 0)

    
    def handle_events(self):
        self.events = pg.event.get()
        self.keys_pressed = pg.key.get_pressed()

    
    def draw(self, screen):
        screen.fill(self.background)
        
        # order matters
        self.draw_group(self.static_bodies, screen)
        self.draw_group(self.projectiles, screen)
        self.draw_group(self.rigid_bodies, screen)
        self.draw_group(self.particles, screen)

    def draw_group(self, group, screen):
        for e in group:
            rect = pg.Rect(e.rect)
            rect.x -= self.camera_shift.x
            rect.y -= self.camera_shift.y
            screen.blit(e.image, rect)

    def start(self):
        pass

    def update(self, dt, t):
        # update camera
        if self.camera_focus != None:
            middle = pg.math.Vector2(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)
            if self.camera_focus.rect.centerx not in range(int(self.game.screen.get_width() / 2) - self.camera_drag, int(self.game.screen.get_width() / 2) + self.camera_drag):
                self.camera_shift.x = self.camera_shift.lerp(pg.math.Vector2(self.camera_focus.rect.centerx), self.camera_acc).x

            needs_update = False
            if self.camera_focus.rect.centerx < middle.x - self.camera_drag: # move camera left
                needs_update = True
            elif self.camera_focus.rect.centerx > middle.x + self.camera_drag: # move camera right
                needs_update = True

            if self.camera_focus.rect.centery < middle.y - self.camera_drag: # move camera up
                needs_update = True
            elif self.camera_focus.rect.centery > middle.y + self.camera_drag: # move camera down
                needs_update = True

            if needs_update:
                self.camera_shift = self.camera_shift.lerp(pg.math.Vector2(self.camera_focus.rect.center) - middle, self.camera_acc)

        for sprite in self.rigid_bodies:
            sprite.update(dt, t)
        for particle in self.particles:
            particle.update(dt, t)

    def close(self):
        pass