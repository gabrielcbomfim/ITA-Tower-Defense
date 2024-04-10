from _ast import arg

import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA
import constants as c
class Enemy(pg.sprite.Sprite):
    """
    Uma classe que representa um inimigo genérico.
    Args:
        waypoints: Lista de pontos (2-tuplas) pelos quais passará o inimigo
        original_image: Imagem original do sprite

    Attributes:
        sprite (pg.sprite.Sprite): The sprite
        waypoints (list): Lista que tuplas guarda os pontos pelos quais passará o inimigo
        pos (Vector2): Posição atual do inimigo
        target_waypoint (int): Qual índice do waypoint é o atual alvo
        speed (float): Velocidade do inimigo
        angle (float): Ângulo do inimigo
        original_image (pygame.image.Image): Imagem original do inimigo
        image (pg.Surface): Imagem atual do inimigo
        rect (Rect): Retângulo que está centrado no inimigo
    """
    def __init__(self,enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0]) 
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["health"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def move(self, world):
        #calculate distance to target
        dist = self.movement.length()

        #check if remaining distance is greater than the enemy speed
        if dist >= (self.speed*world.game_speed):
            self.pos += self.movement.normalize() * (self.speed*world.game_speed)
        else: 
            if dist != 0:
                self.pos += self.movement.normalize() * dist    
            self.target_waypoint += 1    
        
        self.rect.center = self.pos


    def rotate(self, world):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill() #remove instantiate the enemy from screen
            world.health -= 1
            world.missed_enemies += 1

        #calculate distane to next waypoint
        dist = self.target - self.pos
        #use distance to calculate the angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self,world):
        self.rotate(world)
        self.move(world)
        self.check_alive(world)

    def check_alive(self,world):
        if self.health <= 0:
            world.money += c.KILL_REWARD
            world.killed_enemies += 1
            self.kill()
