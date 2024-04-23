import pygame as pg
import math
import constants as c
import turret_data
import turret_data as data
import random
from button import Button
class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, x, y, specific_data):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.buy_cost = specific_data[self.upgrade_level-1]["buy_cost"]
        self.range = specific_data[self.upgrade_level-1]["range"]
        self.cooldown = specific_data[self.upgrade_level-1]["cooldown"]
        self.last_action = pg.time.get_ticks()
        self.selected = False
        self.specific_data = specific_data

        # calculate center coordinates
        self.x = (x+0.5)
        self.y = (y+0.5)

        # animations variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level-1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #create transparent circle showing range
        self.range_image = pg.Surface((self.range*2, self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


    def load_images(self,sprite_sheet):
        #extract images from sprite sheets
        size = sprite_sheet.get_height()
        animation_list = []
        for i in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(i * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def play_animation(self, world):
        #update image
        self.original_image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > (c.ANIMATION_DELAY / world.game_speed):
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record compleded time and clear target so cooldown can start
                self.last_action = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
           surface.blit(self.range_image, self.range_rect)

    def upgrade(self):
        self.upgrade_level += 1
        self.range = self.specific_data[self.upgrade_level-1]["range"]
        self.cooldown = self.specific_data[self.upgrade_level-1]["cooldown"]
        # update animation list
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        # upgrade range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

class TurretRancho(Turret) :

    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretRancho/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_RANCHO_DATA)
        self.food = None
        self.food_type = None

    def create_food(self):
        # TODO
        # Criar sprite de foods
        sprite_food = []
        for i in range(1, 3):
            sprite_food.append(pg.image.load(f"./assets/turrets/TurretRancho/food_{i}.png").convert_alpha())
        self.food_type = random.randint(0, 1)
        self.food = Button(self.x + 10, self.y + 10, sprite_food[self.food_type])

    def update(self, enemy_group, world):
        # TODO
        # Criar dados de cooldown da torre rancho
        if not world.level_started:
            self.last_action = pg.time.get_ticks()
        if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed):
            self.create_food()

    def eat_food(self, player, mouse_pos):
        if self.food is not None:
            if self.food.check_click(mouse_pos):
                if self.food_type:
                   player.change_health(-10)
                else:
                    player.change_health(15)


class TurretAulao(Turret):
    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretAulao/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_AULAO_DATA)


    def update(self, enemy_group, world):
        #if target picked, play firing animation
        if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed):
            self.play_animation(world)

        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    # damage
                    # TODO
                    # ajustar 0.5 (dano da torre em area)
                    enemy.health -= 0.5 * world.game_speed


class TurretGaga(Turret):

    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretGaga/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_GAGA_DATA)
        self.target = None

    def update(self, enemy_group, world):
        #if target picked, play firing animation
        if self.target:
            self.pick_target(enemy_group, world)
            if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed):
                self.play_animation(world)
        else:
            # search for new target once turret has cooled down
            self.pick_target(enemy_group, world)

    def pick_target(self, enemy_group, world):
        #find an enemy to target
        x_dist = 0
        y_dist = 0

        #search for new target
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # damage
                    self.target.health -= c.DAMAGE * world.game_speed
                    break