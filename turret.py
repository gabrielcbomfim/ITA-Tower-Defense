import pygame as pg
import math
import constants as c
import turret_data
import turret_data as data
import random
from button import Button
from animation import Animation
class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, x, y, specific_data):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.damage = specific_data[self.upgrade_level - 1]["damage"]
        self.buy_cost = specific_data[self.upgrade_level - 1]["buy_cost"]
        self.range = specific_data[self.upgrade_level - 1]["range"]
        self.cooldown = specific_data[self.upgrade_level - 1]["cooldown"]
        self.cooldown_natural = self.cooldown
        animation_steps = specific_data[self.upgrade_level - 1]["animation_steps"]
        self.last_action = pg.time.get_ticks()
        self.selected = False
        self.specific_data = specific_data

        # Ability control (pitbull):
        self.pitbull_state = 0
        self.last_state_time = pg.time.get_ticks()


        # calculate center coordinates
        self.x = (x + 0.5)
        self.y = (y + 0.5)

        # animations variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1], animation_steps)
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()


        # update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite sheets
        size = sprite_sheet.get_height()
        animation_list = []

        for i in range(animation_steps):
            temp_img = sprite_sheet.subsurface(i * size, 0, size, size)
            animation_list.append(temp_img)

        return animation_list

    # so esta aqui pq eh chamado em play animation de forma especifica para cada filho
    def action(self, enemy_group):
        pass

    # Realiza a animacao da torre dps ativa a sua acao, seja ela de dano ou dropar comida
    def play_animation(self, world, enemy_group):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > (c.ANIMATION_DELAY / world.game_speed):
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            # if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record compleded time and clear target so cooldown can start
                self.last_action = pg.time.get_ticks()
                self.action(enemy_group)
                self.target = None

    # desenha a torre na tela
    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    # Atualiza os dados da torre dps de um upgrade
    def upgrade(self):
        self.upgrade_level += 1
        self.range = self.specific_data[self.upgrade_level - 1]["range"]
        self.cooldown = self.specific_data[self.upgrade_level - 1]["cooldown"]
        animation_steps = self.specific_data[self.upgrade_level - 1]["animation_steps"]
        # update animation list
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1], animation_steps)
        self.original_image = self.animation_list[self.frame_index]

        # upgrade range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    # interacao do pitbull com as torres
    def pitbull(self):
        self.last_state_time = pg.time.get_ticks()
        self.cooldown_natural = self.cooldown
        self.pitbull_state = 1

    # same
    def pitbull_control(self, player, world):
        if self.pitbull_state == 1:
            self.cooldown = self.cooldown_natural / c.PITBULL_FACTOR
            if pg.time.get_ticks() - self.last_state_time >= c.PITBULL_TIME / world.game_speed:
                self.last_state_time = pg.time.get_ticks()
                self.pitbull_state = 0
                self.cooldown = self.cooldown_natural

# Torre que dropa comida
class TurretRancho(Turret):

    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretRancho/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_RANCHO_DATA)
        self.food = None
        self.food_type = None
        self.eating_audio = pg.mixer.Sound("assets/audio/Audio_Pou_Comendo.wav")

    # Cria a comida
    def create_food(self):
        # TODO
        # Criar sprite de foods
        sprite_food = []
        for i in range(1, 3):
            sprite_food.append(pg.image.load(f"./assets/turrets/TurretRancho/food_{i}.png").convert_alpha())
            sprite_food[i - 1] = pg.transform.scale(sprite_food[i - 1], (100, 100))
        self.food_type = random.randint(0, 1)
        x = self.rect.topleft[0]
        y = self.rect.topleft[1]
        self.food = Button(x + 25, y - 10, sprite_food[self.food_type])

    # atualizacao para cada frame do jogo
    def update(self, enemy_group, world):
        # TODO
        # Criar dados de cooldown da torre rancho
        if not world.level_started:
            self.last_action = pg.time.get_ticks()
        if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed):
            self.create_food()
            self.last_action = pg.time.get_ticks()
        self.pitbull_control(self, world)

    # desenha a torre, e a comida se houver alguma
    def draw(self, surface):
        super().draw(surface)
        if self.food is not None:
            self.food.draw(surface)

    # aplica os efeitos da comida no player
    def eat_food(self, player, mouse_pos):
        if self.food is not None:
            if self.food.check_click(mouse_pos):
                self.eating_audio.play()
                if self.food_type:
                    player.change_health(-10)
                else:
                    player.change_health(15)
                self.food = None
                return True
        return False

# Torre que da dano em area
class TurretAulao(Turret):
    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretAulao/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_AULAO_DATA)
        self.target = None


        # parte realitva a animacao do dano em area
        self.boomimage = pg.image.load(f"./assets/turrets/TurretAulao/boomaulao.png").convert_alpha()
        self.boom_list = self.load_boom()
        self.boom = None
        self.create_animation()


    # atualiacao a cada frame do jogo
    def update(self, enemy_group, world):
        # if target picked, play firing animation
        if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed) and self.target:
            self.play_animation(world, enemy_group)
        else:
            self.pick_target(enemy_group, world)
            self.boom.frame_index = 0
        self.pitbull_control(self, world)

    # faz a animacao da torre e do ataque
    def play_animation(self, world, enemy_group):
        super().play_animation(world, enemy_group)
        self.boom.update()

    # carrega os dados do sprite do ataque
    def load_boom(self):
        # extract images from sprite sheets
        sprite_width = self.boomimage.get_width()
        sprite_height = self.boomimage.get_height()

        sprite_width = sprite_width * 2
        sprite_height = sprite_height * 2
        self.boomimage = pg.transform.scale(self.boomimage, (sprite_width, sprite_height))
        boom_list = []

        for i in range(5):

            temp_img = self.boomimage.subsurface(i * sprite_height/2, 0, sprite_height/2, sprite_height/2)
            boom_list.append(temp_img)
        for i in range(3):
            temp_img = self.boomimage.subsurface(i * sprite_height/2, sprite_height/2, sprite_height/2, sprite_height/2)
            boom_list.append(temp_img)


        return boom_list

    # define o boom como um objeto animacao
    def create_animation(self):
        self.boom = Animation(self.x, self.y, self.boom_list)

    # desenha o a torre e o ataque
    def draw(self, surface):
        super().draw(surface)
        sprite_width = self.boom_list[0].get_width()
        if self.boom is not None:
            self.boom.draw(surface,self.x - sprite_width/2,self.y - sprite_width/2)

    # verifica se ha algum inimigo proximo
    def pick_target(self, enemy_group, world):
        # search for new target
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    break

    # ataca em area houver algum inimigo proximo
    def action(self, enemy_group):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    # damage
                    # TODO
                    # ajustar 0.5 (dano da torre em area)
                    enemy.health -= self.damage

# torre que da dano single target
class TurretGaga(Turret):

    def __init__(self, x, y):
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretGaga/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_GAGA_DATA)
        self.target = None

    # atualiza a cada frame do jogo
    def update(self, enemy_group, world):
        # if target picked, play firing animation
        if self.target:
            self.pick_target(enemy_group, world)
            if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed):
                self.play_animation(world, enemy_group)
        else:
            # search for new target once turret has cooled down
            self.pick_target(enemy_group, world)
        self.pitbull_control(self, world)

    # verifica se ha algum alvo proximo
    def pick_target(self, enemy_group, world):
        # search for new target
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    break

    # ataca o primeiro alvo a entrar no range da torre
    def action(self, enemy_group):
        if self.target:
            self.target.health -= self.damage
