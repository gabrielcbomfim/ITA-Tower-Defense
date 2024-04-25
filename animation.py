import pygame as pg
import math
import constants as c
import turret_data
import turret_data as data
import random
from button import Button

#classe para animação das torres e inimigos
class Animation():
    def __init__(self,x, y, images):

        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.animation_cooldown = 2000

    def update(self):
        # update animation
        # update image
        self.image = self.images[self.frame_index]
        # check if it's time to update the frame
        self.frame_index += 1
        # if the animation has run out then reset
        if self.frame_index >= len(self.images):
            self.frame_index = 0
            self.image = self.images[self.frame_index]

    def draw_instant(self, surface, x, y):
        # Draw one frame of the animation at a time
        while (self.frame_index < len(self.images)):

            image = self.images[self.frame_index]
            rect = image.get_rect()
            rect.topleft = (x, y)
            surface.blit(image, rect)
            # Update the screen to show the current frame
            pg.display.flip()
            # Wait for a short time before drawing the next frame
            pg.time.delay(15)  # Delay in milliseconds (adjust as needed)
            self.frame_index += 1

    def draw(self, surface,x,y):
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # draw image
        surface.blit(self.image, self.rect)

    #update position from enemie
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

    def load_image(self, number_of_sprites):
# extract images from sprite sheets
        sprite_width = self.image.get_width()
        sprite_height = self.image.get_height()

        sprite_width = sprite_width
        sprite_height = sprite_height
        self.boomimage = pg.transform.scale(self.image, (sprite_width, sprite_height))
        boom_list = []

        for i in range(number_of_sprites):
            temp_img = self.boomimage.subsurface(i * sprite_height, 0, sprite_height, sprite_height)
            boom_list.append(temp_img)

        self.images = boom_list
