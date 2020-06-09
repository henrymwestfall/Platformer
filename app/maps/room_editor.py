import sys
import os
import pickle

import pygame as pg

TILE_SIZE = 32
MAP_WIDTH = 128
MAP_HEIGHT = 64
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

TILE_COLOR = (34, 139, 34)
TILE = pg.Surface([TILE_SIZE, TILE_SIZE])
TILE.fill(TILE_COLOR)

EDGE = pg.Surface([TILE_SIZE, TILE_SIZE])
EDGE.fill((0, 0, 0))

COIN = pg.Surface([16, 16])
pg.draw.circle(COIN, (255, 255, 0), (8, 8), 8)

MAP_NAME = "CombatTest"

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()

map_surface = pg.Surface([TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT])
map_surface.fill((128, 198, 229))
map_rect = map_surface.get_rect()

if not os.path.exists(f"{MAP_NAME}.map"):
    current_map = [[0 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
else:
    with open(f"{MAP_NAME}.map", "rb") as f:
        current_map = pickle.load(f)

def finish():
    pg.quit()
    do_save = None
    while not (do_save in ["y", "n"]):
        do_save = input("Save map? [y/n] ")
        if do_save == "y":
            with open(f"{MAP_NAME}.map", "wb") as f:
                pickle.dump(current_map, f)
        elif do_save == "n":
            pass
        else:
            print("invalid response")
    sys.exit()

def fill_recursive(source, visited=[]):
    visited.append(source)
    if current_map[int(source.x)][int(source.y)] == 0:
        neighbors = []
        for x, row in enumerate(current_map):
            for y, cell in enumerate(row):
                if abs(source.x - x) + abs(source.y - y) == 1:
                    neighbors.append(pg.math.Vector2(x, y))

        for n in neighbors:
            if n in visited:
                continue
            fill_recursive(n, visited)
    return visited

camera_x = 0
camera_y = 0
camera_speed = 1000

section_path_start = None

while True:
    dt = clock.tick(60) / 1000.0
    events = pg.event.get()
    mouse_pos = pg.mouse.get_pos()
    drawing = bool(pg.mouse.get_pressed()[0])
    erasing = bool(pg.mouse.get_pressed()[2])
    
    cleared = True
    if any([1 in row for row in current_map]):
        cleared = False

    for evt in events:
        if evt.type == pg.QUIT:
            finish()

    pressed = pg.key.get_pressed()
    if pressed[pg.K_UP]:
        camera_y += camera_speed * dt
    elif pressed[pg.K_DOWN]:
        camera_y -= camera_speed * dt

    if pressed[pg.K_c]: # clear
        current_map = [[0 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    if pressed[pg.K_r]: # relic
        focus = pg.math.Vector2(mouse_pos)
        focus.x = (focus.x - camera_x) // TILE_SIZE
        focus.y = (focus.y - camera_y) // TILE_SIZE

        try:
            current_map[int(focus.x)][int(focus.y)] = 2
        except IndexError:
            pass
    
    if pressed[pg.K_e]:
        focus = pg.math.Vector2(mouse_pos)
        focus.x = (focus.x - camera_x) // TILE_SIZE
        focus.y = (focus.y - camera_y) // TILE_SIZE

        try:
            current_map[int(focus.x)][int(focus.y)] = 3
        except IndexError:
            pass

    if pressed[pg.K_f]: # fill recursively
        if not cleared:
            focus = pg.math.Vector2(mouse_pos)
            focus.x = (focus.x - camera_x) // TILE_SIZE
            focus.y = (focus.y - camera_y) // TILE_SIZE

            try:
                visited = fill_recursive(focus)
            except RecursionError:
                print("fill area too large")
                visited = []
            for v in visited:
                current_map[int(v.x)][int(v.y)] = 1
        else:
            current_map = [[1 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
    
    
    if pressed[pg.K_RIGHT]:
        camera_x -= camera_speed * dt
    elif pressed[pg.K_LEFT]:
        camera_x += camera_speed * dt

    if drawing or erasing:
        focus = pg.math.Vector2(mouse_pos)
        focus.x = (focus.x - camera_x) // TILE_SIZE
        focus.y = (focus.y - camera_y) // TILE_SIZE
        try:
            if drawing:
                current_map[int(focus.x)][int(focus.y)] = 1
            elif erasing:
                current_map[int(focus.x)][int(focus.y)] = 0
        except IndexError:
            pass

    screen.fill((255, 255, 255))
    map_render_rect = pg.Rect(map_rect)
    map_render_rect.x += camera_x
    map_render_rect.y += camera_y
    screen.blit(map_surface, map_render_rect)

    # draw the tiles
    for x, row in enumerate(current_map):
        for y, cell in enumerate(row):
            rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            rect.x += camera_x
            rect.y += camera_y
            if cell == 1:
                screen.blit(TILE, rect)
            elif cell == 2:
                screen.blit(COIN, rect)
            elif cell >= 3:
                screen.blit(EDGE, rect)
    
    pg.display.flip()