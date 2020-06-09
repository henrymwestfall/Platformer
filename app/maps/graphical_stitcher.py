import os
import pickle

import pygame as pg

WHITE = (255, 255, 255)
FOREST_GREEN = (34, 139, 34)

def load_tile_map(name, *subdirs):
    if ".pkl" in name:
        file_name = name
    else:
        file_name = name + ".pkl"
    path = os.path.join(*subdirs, name)
    with open(path, "rb") as f:
        raw_data = pickle.load(f)
    return raw_data

TILE_SIZE = 8

pg.init()
screen = pg.display.set_mode([1200, 900])
screen.fill(WHITE)
clock = pg.time.Clock()

working_directory = "DemoArea"#input("What subdirectory are the map files located in? ")
os.chdir(working_directory)

# load maps from working directory
all_maps = [m for m in os.listdir() if m.endswith(".map")]
map_sprites = []
for z, m in enumerate(all_maps):
    raw_map_data = load_tile_map(m)
    height = 0
    width = 0
    rects = []
    full_canvas = pg.Surface([TILE_SIZE * len(raw_map_data), TILE_SIZE * len(raw_map_data[0])])
    for x, line in enumerate(raw_map_data):
        for y, cell in enumerate(line):
            if int(cell) == 1:
                rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(full_canvas, FOREST_GREEN, rect)
                
            elif cell >= 1000:
                pg.draw.rect(full_canvas, (255, 0, 0), rect)
            else:
                continue
                
            height = max([height, y + 1])
            width = max([width, x + 1])
            
    image = pg.Surface([width * TILE_SIZE, height * TILE_SIZE])
    for rect in rects:
        pg.draw.rect(image, FOREST_GREEN, rect)
    map_sprites.append((image, image.get_rect(), z))

# define camera
camera = pg.math.Vector2(0, 0)
camera_speed = 1000

focus = None
mouse_offset_to_focus = pg.math.Vector2(0, 0)

while True:
    dt = clock.tick(60) / 1000.0

    events = pg.event.get()
    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()
    shifted_mouse_position = pg.math.Vector2(pg.mouse.get_pos()) - camera

    # handle camera shift
    if keys_pressed[pg.K_w]:
        camera.y -= camera_speed * dt
    elif keys_pressed[pg.K_s]:
        camera.y += camera_speed * dt

    if keys_pressed[pg.K_a]:
        camera.x -= camera_speed * dt
    elif keys_pressed[pg.K_d]:
        camera.x += camera_speed * dt

    # determine or move focus
    if not mouse_pressed[0]:
        focus = None

    if focus == None and mouse_pressed[0]:
        highest = None
        for sprite in map_sprites:
            image, rect, z = sprite
            if rect.collidepoint(shifted_mouse_position):
                if highest == None:
                    highest = sprite
                elif z > highest[2]:
                    highest = sprite
        if highest != None:
            focus = highest
            mouse_offset_to_focus = pg.math.Vector2(highest[1].topleft) - shifted_mouse_position
    elif focus != None:
        focus[1].topleft = mouse_offset_to_focus + shifted_mouse_position

    screen.fill(WHITE)
    # draw everything
    for sprite in sorted(map_sprites, key=lambda s: s[2], reverse=True):
        rect = pg.Rect(sprite[1])
        rect.topleft = pg.math.Vector2(rect.topleft) - camera
        screen.blit(sprite[0], rect)

    pg.display.flip()