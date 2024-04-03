import json
import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()


#create game window
# Size bizu: 1580, 860
screen = pg.display.set_mode((1580, 860), pg.FULLSCREEN)
pg.display.set_caption("ITAwer Defense")

# Game Variables
placing_turrets = False

#load images
# Map:
map_image = pg.image.load("./assets/mapa/mapa4.png")
map_image_resized = pg.transform.scale(map_image, (screen.get_width(), screen.get_height()))
# Enemies:
enemy_image = pg.image.load("./enemy_1.png")
#individual turret image for mouse cursor
cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()
# Buttons:
buy_turrent_image = pg.image.load("./assets/buttons/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()

#load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
    turret_group.add(turret)


# Create world
world = World(screen, world_data, map_image_resized)


# Enemies groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create enemies
enemy = Enemy(world.paths[5], enemy_image)
enemy_group.add(enemy)

# Create buttons:
turrent_button = Button(1030, 120, buy_turrent_image)
cancel_button = Button(1030, 180, cancel_image)

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

    #draw buttons:
    if turrent_button.draw(screen):
        placing_turrets = True

    # if placing turrents then show the cancel button as well
    if placing_turrets:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDHT:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen) or pg.mouse.get_pressed()[2] == 1:
            placing_turrets = False

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

        # Mouse Click:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and placing_turrets:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the game area
            if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
                pass
            create_turret(mouse_pos)




    #update the display
    pg.display.flip()
    

pg.quit()
 