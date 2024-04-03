import json
import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
from turret_shop import TurretShop
from button import Button
import constants as c

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()


#create game window
# Size bizu: 1580, 860
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
pg.display.set_caption("ITAwer Defense")

#load images
# Map:
map_image = pg.image.load("./assets/mapa/mapa4.png")
map_image_resized = pg.transform.scale(map_image, (screen.get_width(), screen.get_height()))
# Enemies:
enemy_image = pg.image.load("./enemy_1.png")

#load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)


# Create world
world = World(screen, world_data, map_image_resized)

# Create turret shop
turret_shop = TurretShop(world)

# Enemies groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create enemies
enemy = Enemy(world.paths[5], enemy_image)
enemy_group.add(enemy)

# Game loop
run = True
while run:

    clock.tick(c.FPS)

    ##########################
    # UPDATING SECTION
    ##########################

    # update groups
    enemy_group.update()

    ##########################
    # DRAWING SECTION
    ##########################
    screen.fill("grey100")

    #draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen, "grey0", False, world.paths[5])

    #Draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    #draw UI
    turret_shop.draw(screen)

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

        # Mouse Click:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and turret_shop.placing_turrets:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the game area
            if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
                pass
            turret_shop.create_turret(mouse_pos, turret_group)




    #update the display
    pg.display.flip()
    

pg.quit()
 