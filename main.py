import json
import pygame as pg
from enemy import Enemy
from turret import TurretRancho
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
    "weak": pg.image.load("./assets/enemies/computador.png"),
    "medium": pg.image.load("assets/enemies/paper.png"),
    "strong": pg.image.load("./assets/enemies/airplane.png"),
    "elite": pg.image.load("./assets/enemies/inferninho.png")
}
#Audio

game_over_audio = pg.mixer.Sound("assets/audio/Game Over sound effect.mp3")
#turret_sheet = pg.image.load("./assets/turrets/turret_1.png").convert_alpha()
# load json data for level
with open('assets/mapa/mapaTiled/level_data.tmj') as file:
    world_data = json.load(file)

#Primeira tocada de musica lenta:
pg.mixer.music.load('assets/audio/CovaDela90BPM.wav')
pg.mixer.music.play(-1)

# Restart loop, only quits on pg.QUIT
while True:

    update_time = 0
    path_aleatorio = 0

    # Create world
    world = World(screen, world_data, map_image_resized)
    world.process_data()
    world.process_enemies()

    # Enemies groups
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # Player
    player = Player(turret_group, world, enemy_group)

    inferninho_no_ultimo_level = False
    inferninho_ja_ocorreu = False

    # Game loop
    while player.run:

        clock.tick(c.FPS)

        ##########################
        # UPDATING SECTION
        ##########################

        if not world.game_over:
            # check if player has lost
            if player.i_count > c.I_LIMIT:
                pg.mixer.music.load('assets/audio/CovaDela90BPM.wav')
                pg.mixer.music.play(0)
                world.game_outcome = -1
                world.game_over = True
                # add music

                game_over_audio.play()


        # update groups
        if not world.level_started:
            update_time = pg.time.get_ticks()
        if pg.time.get_ticks() - update_time > (c.PATH_RELOADO_TIME / world.game_speed):
            update_time = pg.time.get_ticks()
            path_aleatorio = random.randint(1, len(world.paths) - 1)

        enemy_group.update(player, world)
        turret_group.update(enemy_group, world)

        player.update(world)

        ##########################
        # DRAWING SECTION
        ##########################
        screen.fill("grey100")

        # draw level
        world.draw(screen)

        # draw enemy path
        #pg.draw.lines(screen, "grey0", False, world.paths[path_aleatorio])

        # Draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        player.draw_ui(screen)



        if not world.game_over:


            if world.level_started:

                if inferninho_no_ultimo_level:
                    world.level = semestre_atual + 1
                    inferninho_no_ultimo_level = False

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

                # Muito bronco, mas ta funcionando
                if not world.game_over:
                    # check if player has won
                    if world.level == c.TOTAL_LEVELS and world.check_level_complete():
                        world.game_outcome = 1
                        pg.mixer.music.play(0)
                        pg.mixer.music.load('assets/audio/You are my sunshine Lebron James meme.mp3')
                        pg.mixer.music.play(1)
                        world.game_over = True

                player.money += c.LEVEL_COMPLETE_REWARD
                world.level_started = False
                # Tocar musica calma:
                if world.level != 10:
                    pg.mixer.music.play(0)
                    pg.mixer.music.load('assets/audio/CovaDela90BPM.wav')
                    pg.mixer.music.play(-1)

                inferninho_probabilidade = 0
                if player.i_count > 1:
                    inferninho_probabilidade = random.randint(1, 6 - player.i_count)
                if inferninho_probabilidade == 1 and not inferninho_ja_ocorreu:
                    inferninho_no_ultimo_level = True
                    inferninho_ja_ocorreu = True
                    semestre_atual = world.level
                    world.level = 11
                elif world.level < 10:
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
            if player.handle_input(event,screen):
                break



        # update the display
        pg.display.flip()

    if not player.restart:
        break

pg.quit()
