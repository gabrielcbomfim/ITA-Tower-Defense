import pygame
import pygame as pg
import constants as c
from enemy import Enemy
from world import World
 
#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
#screen = pg.display.set_mode((c.SCREEN_WIDHT, c.SCREEN_HEIGHT))
screen = pg.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pg.display.set_caption("ITAwer Defense")

#load images
enemy_image = pg.image.load("./enemy_1.png")
map_image = pg.image.load("./assets/mapa/mapa1.png")
map_image_resized = pg.transform.scale(map_image, (screen.get_width(), screen.get_height()))

# Create world
world = World(map_image_resized)

#enemy path
waypoints = [(100, 100),
            (300, 250),
            (480, 150),
            (220, 50),
            (45, 40),
            (45, 300)]


# Enemies groups
enemy_group = pg.sprite.Group()
enemy = Enemy(waypoints, enemy_image)
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
    pg.draw.lines(screen, "grey0", False, waypoints)

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
 