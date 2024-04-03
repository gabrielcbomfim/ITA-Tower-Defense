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
selected_turret = None


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


#turret spritesheets
turret_spritesheets = []
for x in range (1, c.TURRET_LEVELS+1):
    turret_spritesheets.append(pg.image.load(f"./assets/turrets/turret_{x}.png").convert_alpha())


turret_sheet = pg.image.load("./assets/turrets/turret_1.png").convert_alpha()
#individual turret image for mouse cursor
cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()
# Buttons:
buy_turrent_image = pg.image.load("./assets/buttons/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()
upgrade_turret_image = pg.image.load("./assets/buttons/upgrade_turret.png").convert_alpha()


#load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
    turret_group.add(turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if abs(turret.tile_x - mouse_tile_x)<=20 and abs(turret.tile_y - mouse_tile_y)<=20:
            turret.selected = True
            return turret
def clear_selection():
    for turret in turret_group:
        turret.selected = False

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


# Create buttons:
turrent_button = Button(1230, 120, buy_turrent_image)
cancel_button = Button(1230, 180, cancel_image)
upgrade_button = Button(1205, 180, upgrade_turret_image)


# Game loop
run = True
while run:

    clock.tick(c.FPS)

    ##########################
    # UPDATING SECTION
    ##########################

    # update groups
    enemy_group.update()
    turret_group.update(enemy_group)

    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True
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
    for turret in turret_group:
        turret.draw(screen)



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
    # if a turret is selected then show the upgrade button\
    if selected_turret:
        #if a turret is selected then show the upgrade button
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()

    #draw UI
    turret_shop.draw(screen)


    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

        # Mouse Click:

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the game area
            if mouse_pos[0] < c.SCREEN_WIDHT and mouse_pos[1] < c.SCREEN_HEIGHT:
                #clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and turret_shop.placing_turrets:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the game area
            if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
                pass
            turret_shop.create_turret(mouse_pos, turret_group)





    #update the display
    pg.display.flip()
    

pg.quit()
 