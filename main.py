import json
import pygame as pg
import constants as c
from enemy import Enemy
from world import World


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

#load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)

# Create world
world = World(screen, world_data, map_image_resized)
world.process_data()



# Enemies groups
enemy_group = pg.sprite.Group()
enemy = Enemy(world.paths[0], enemy_image)
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
    pg.draw.lines(screen, "grey0", False, world.paths[0])

    #update groups
    enemy_group.update()

    #draw enemies group
    enemy_group.draw(screen)

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

    #update the display
    pg.display.flip()
    

pg.quit()
 