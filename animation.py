import pygame as pg
import math
import constants as c
import turret_data
import turret_data as data
import random
from button import Button

class Animation():
    def __init__(self,x, y, images, frame_duration):

        self.images = images
        self.frame_duration = frame_duration
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


    def draw(self, surface,x,y):
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # draw image
        surface.blit(self.image, self.rect)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)