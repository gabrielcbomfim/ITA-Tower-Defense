from _ast import arg

import math
import pygame as pg
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
import constants as c
from player import Player


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

    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.type = enemy_type
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0

        # direction for the enemy
        # 0 = down, 1 = up, 2 = right, 3 = left
        # nasce sempre para direita.
        self.direction = 2




        # self.original_image = images.get(enemy_type)


        # animations variables
        self.sprite_sheet = images.get(enemy_type)

        self.animation_list, self.animation_lists = self.load_images(self.sprite_sheet)

        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.image = pg.transform.rotate(self.animation_list[self.frame_index], self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def load_images(self, sprite_sheet):
        # Extract images from sprite sheets
        sprite_width = sprite_sheet.get_width()
        sprite_height = sprite_sheet.get_height()
        animation_list = []
        animation_lists = []

        if self.type == "weak":
            sprite_width = sprite_width/5
            sprite_height = sprite_height/5
            animation_list.append(pg.transform.scale(sprite_sheet, (sprite_width, sprite_height)))
        elif self.type == "medium":
            sprite_width = sprite_width*1.5
            sprite_height = sprite_height*1.5
            sprite_sheet = pg.transform.scale(sprite_sheet, (sprite_width, sprite_height))
            animation_steps = 3
            for x in range(animation_steps):
                temp_img = sprite_sheet.subsurface(x * sprite_width/3, 0, sprite_width/3, sprite_height)
                animation_list.append(temp_img)
        elif self.type == "strong":
            animation_steps = 2
            for x in range(animation_steps):
                temp_img = sprite_sheet.subsurface(x * sprite_width/2, 0, sprite_width/2, sprite_height)
                animation_list.append(temp_img)
        elif self.type == "elite":
            sprite_width = sprite_width*2
            sprite_height = sprite_height*2
            sprite_sheet = pg.transform.scale(sprite_sheet, (sprite_width, sprite_height))
            animation_steps = 4
            for y in range(4):
                animation_list = []
                for x in range(animation_steps):
                    temp_img = sprite_sheet.subsurface(x * sprite_width/4, y * sprite_height/4, sprite_width/4, sprite_height/4)
                    animation_list.append(temp_img)
                animation_lists.append(animation_list)
            animation_list = animation_lists[self.direction]
        return animation_list, animation_lists


    def play_animation(self, world):
        if self.type == "elite":
            if self.direction == 0:
                self.animation_list = self.animation_lists[0]
            elif self.direction == 1:
                self.animation_list = self.animation_lists[1]
            elif self.direction == 2:
                self.animation_list = self.animation_lists[2]
            elif self.direction == 3:
                self.animation_list = self.animation_lists[3]

        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > (c.ANIMATION_ENEMY_DELAY / (self.speed * world.game_speed)):
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def move(self, world):
        # calculate distance to target
        dist = self.movement.length()

        # check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.pos

    def rotate(self, player, world):
        # define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()  # remove instantiate the enemy from screen
            player.add_i()
            world.missed_enemies += 1

        # calculate distane to next waypoint
        dist = self.target - self.pos
        # use distance to calculate the angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotate image and update rectangle
        if self.type == "weak":
            if self.angle < 45 and self.angle > -45:
                self.image = pg.transform.rotate(self.animation_list[self.frame_index], 90)
            elif self.angle < 135 and self.angle > 45:
                self.image = pg.transform.rotate(self.animation_list[self.frame_index], 0)
            elif self.angle < -45 and self.angle > -135:
                self.image = pg.transform.rotate(self.animation_list[self.frame_index], 0)
            elif self.angle < -135 or self.angle > 135:
                self.image = pg.transform.rotate(self.animation_list[self.frame_index],  90)
        elif self.type != "elite":
            self.image = pg.transform.rotate(self.animation_list[self.frame_index], self.angle - 90)
        else:
            if self.angle < 45 and self.angle > -45:
                self.direction = 2
            elif self.angle < 135 and self.angle > 45:
                self.direction = 1
            elif self.angle < -45 and self.angle > -135:
                self.direction = 0
            elif self.angle < -135 or self.angle > 135:
                self.direction = 3


        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, player, world):
        self.play_animation(world)
        self.rotate(player, world)
        self.move(world)
        self.check_alive(player, world)

    def check_alive(self, player, world):
        if self.health <= 0:
            player.money += c.KILL_REWARD
            world.killed_enemies += 1
            self.kill()



