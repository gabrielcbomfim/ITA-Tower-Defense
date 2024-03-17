import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0]) 
        self.target_waypoint = 1
        self.speed = 1.2
        self.angle = 0
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move(self):
        #calculate distance to target
        dist = self.movement.length()

        #check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else: 
            if dist != 0:
                self.pos += self.movement.normalize() * dist    
            self.target_waypoint += 1    
        
        self.rect.center = self.pos

    def rotate(self):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill() #remove instantiate the enemy from screen

        #calculate distane to next waypoint
        dist = self.target - self.pos
        #use distance to calculate the angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.rotate()
        self.move()