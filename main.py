import pygame as pg
import constants as c
from enemy import Enemy

 
#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDHT, c.SCREEN_HEIGHT))
pg.display.set_caption("ITAwer Defense")

#load images
enemy_image = pg.image.load("./enemy_1.png")

#enemy path
waypoints = [(100, 100),
            (300, 250),
            (480, 150),
            (220, 50),
            (45, 40),
            (45, 300)]

#enemies groups
enemy_group = pg.sprite.Group()
enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

#game loop
run = True
while run:
    
    clock.tick(c.FPS)

    #clean enemie's walking
    screen.fill("grey100")

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
 