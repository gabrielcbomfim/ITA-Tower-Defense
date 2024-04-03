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
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
pg.display.set_caption("ITAwer Defense")

# Game Variables
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

#load images
# Map:
map_image = pg.image.load("./assets/mapa/mapa4.png")
map_image_resized = pg.transform.scale(map_image, (screen.get_width(), screen.get_height()))
# Enemies:
enemy_images = {
    "weak": pg.image.load("./assets/enemies/enemy_1.png"),
    "medium": pg.image.load("./assets/enemies/enemy_2.png"),
    "strong": pg.image.load("./assets/enemies/enemy_3.png"),
    "elite": pg.image.load("./assets/enemies/enemy_4.png")
}


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


# Enemies groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create buttons:
turrent_button = Button(c.SCREEN_WIDHT+30, 120, buy_turrent_image)
cancel_button = Button(c.SCREEN_WIDHT+30, 180, cancel_image)
upgrade_button = Button(c.SCREEN_WIDHT+5, 180, upgrade_turret_image)

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

    #Spawn enemies
    if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.paths[5], enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()


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



    #update the display
    pg.display.flip()
    

pg.quit()
 