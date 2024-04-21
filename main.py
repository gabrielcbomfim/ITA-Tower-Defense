import json
import pygame as pg
from enemy import Enemy
from world import World
from player import Player
import constants as c

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

# load fonts for text on screen
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)


# font for outputting text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Game Variables
game_over = False
game_outcome = 0  # -1 is loss, 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()

# Create world
world = World(screen, world_data, map_image_resized)
world.process_data()
world.process_enemies()

# Enemies groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Player
player = Player(turret_group, turret_spritesheets, world)


# restarts the game
def restart():

    # Game Variables
    global game_over
    global game_outcome
    global level_started
    global last_enemy_spawn
    game_over = False
    game_outcome = 0  # -1 is loss, 1 is win
    level_started = False
    last_enemy_spawn = pg.time.get_ticks()

    # Create world
    global world
    world = World(screen, world_data, map_image_resized)
    world.process_data()
    world.process_enemies()

    # Enemies groups
    global enemy_group
    global turret_group
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # Player
    global player
    player = Player(turret_group, turret_spritesheets, world)


# Game loop
run = True
while run:

    clock.tick(c.FPS)

    ##########################
    # UPDATING SECTION
    ##########################

    if not game_over:
        # check if player has lost
        if player.health <= 0:
            game_outcome = -1
            game_over = True
        # check if player has won
        if world.level == c.TOTAL_LEVELS and world.check_level_complete():
            game_outcome = 1
            game_over = True

    # update groups
    enemy_group.update(player, world)
    turret_group.update(enemy_group, world)

    # highlight selected turret
    if player.selected_turret:
        player.selected_turret.selected = True

    ##########################
    # DRAWING SECTION
    ##########################
    screen.fill("grey100")

    # draw level
    world.draw(screen)

    # draw enemy path
    pg.draw.lines(screen, "grey0", False, world.paths[5])

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    draw_text(str(player.health), text_font, "grey100", 0, 0)
    draw_text(str(player.money), text_font, "grey100", 0, 30)
    draw_text(str(world.level), text_font, "grey100", 0, 60)

    if not game_over:

        # check if the level started or not
        if not level_started:
            if player.begin_button.draw(screen):
                level_started = True

        else:
            # speed up the game
            world.game_speed = 1
            if player.fast_forward_button.draw(screen):
                world.game_speed = 2
            # Spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.paths[5], enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # check if the wave is finished
        if world.check_level_complete():
            player.money += c.LEVEL_COMPLETE_REWARD
            level_started = False
            world.level += 1
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

        player.draw_ui(screen)

    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey100", 310, 250)
        elif game_outcome == 1:
            draw_text("YOU WIN", large_font, "grey100", 315, 250)
        # restart button
        if player.restart_button.draw(screen):
            restart()

    # event handler
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False
            break

        # sends event to UI
        if player.handle_input(event):
            break

    # update the display
    pg.display.flip()

pg.quit()
