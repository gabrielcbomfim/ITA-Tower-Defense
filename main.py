import json
import pygame as pg
from enemy import Enemy
from world import World
from player import Player
import constants as c
import random

# initialise pygame
pg.init()

# create clock
clock = pg.time.Clock()

# create game window
screen = pg.display.set_mode((1920, 1080), pg.SCALED | pg.FULLSCREEN)

pg.display.set_caption("ITAwer Defense")


# load images
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

# turret spritesheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_spritesheets.append(pg.image.load(f"./assets/turrets/turret_{x}.png").convert_alpha())

turret_sheet = pg.image.load("./assets/turrets/turret_1.png").convert_alpha()
# load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)

# Restart loop, only quits on pg.QUIT
while True:

    update_time = 0
    path_aleatorio = 5

    # Create world
    world = World(screen, world_data, map_image_resized)
    world.process_data()
    world.process_enemies()

    # Enemies groups
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # Player
    player = Player(turret_group, turret_spritesheets, world)

    # Game loop
    while player.run:

        clock.tick(c.FPS)

        ##########################
        # UPDATING SECTION
        ##########################

        if not world.game_over:
            # check if player has lost
            if player.health <= 0:
                world.game_outcome = -1
                world.game_over = True
            # check if player has won
            if world.level == c.TOTAL_LEVELS and world.check_level_complete():
                world.game_outcome = 1
                world.game_over = True

        # update groups
        if not world.level_started:
            update_time = pg.time.get_ticks()
        if pg.time.get_ticks() - update_time > (c.PATH_RELOADO_TIME / world.game_speed):
            update_time = pg.time.get_ticks()
            path_aleatorio = random.randint(1, len(world.paths) - 1)

        enemy_group.update(player, world)
        turret_group.update(enemy_group, world)

        player.update()

        ##########################
        # DRAWING SECTION
        ##########################
        screen.fill("grey100")

        # draw level
        world.draw(screen)


        # draw enemy path
        pg.draw.lines(screen, "grey0", False, world.paths[path_aleatorio])

        # Draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        player.draw_ui(screen)

        if not world.game_over:
            if world.level_started:
                # Spawn enemies
                if pg.time.get_ticks() - world.last_enemy_spawn > c.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.paths[path_aleatorio], enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        world.last_enemy_spawn = pg.time.get_ticks()

            # check if the wave is finished
            if world.check_level_complete():
                player.money += c.LEVEL_COMPLETE_REWARD
                world.level_started = False
                world.level += 1
                world.last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()

        # event handler
        for event in pg.event.get():
            # quit program
            if event.type == pg.QUIT:
                player.run = False
                player.restart = False
                break

            # sends event to UI
            if player.handle_input(event):
                break

        # update the display
        pg.display.flip()

    if not player.restart:
        break

pg.quit()
