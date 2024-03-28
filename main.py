import json
import pygame as pg
import constants as c
from enemy import Enemy
from world import World
from turret import Turret


#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()


#create game window
# Size bizu: 1580, 860
screen = pg.display.set_mode((1580, 860), pg.FULLSCREEN)
pg.display.set_caption("ITAwer Defense")

#load images
enemy_image = pg.image.load("./enemy_1.png")
map_image = pg.image.load("./assets/mapa/mapa4.png")
map_image_resized = pg.transform.scale(map_image, (screen.get_width(), screen.get_height()))
#individual turret image for mouse cursor
cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()

#load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    turret = Turret(cursor_turret, mouse_pos)
    turret_group.add(turret)


# Create world
world = World(screen, world_data, map_image_resized)


# Enemies groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.paths[5], enemy_image)
enemy_group.add(enemy)

# Game loop
run = True
while run:

    clock.tick(c.FPS)

    #clean enemie's walking
    screen.fill("grey100")

    #draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen, "grey0", False, world.paths[5])

    #update groups
    enemy_group.update()

    #draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

        # Mouse Click:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the game area
            if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
                create_turret(mouse_pos)


    #update the display
    pg.display.flip()
    

pg.quit()
 