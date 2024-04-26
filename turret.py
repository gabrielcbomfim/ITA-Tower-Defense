import pygame as pg
import math
import constants as c
import turret_data
import turret_data as data
import random
from button import Button
from animation import Animation
class Turret(pg.sprite.Sprite):
    """
       Classe base para todas as torres do jogo.
    """
    def __init__(self, sprite_sheets, x, y, specific_data):
        """
                 Inicializa uma torre com os parâmetros fornecidos.

                Args:
                - sprite_sheets: lista de spritesheets da torre para diferentes níveis de atualização
                - x, y: coordenadas da torre no jogo
                - specific_data: dados específicos da torre (dano, custo, alcance, etc.) para diferentes níveis de atualização
        """
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
        """
                Extrai imagens do spritesheet da torre para a animação.

                Args:
                - sprite_sheet: spritesheet da torre para um nível específico de atualização
                - animation_steps: número de etapas de animação

                Returns:
                - animation_list: lista de imagens de animação da torre
        """
        # extract images from sprite sheets
        size = sprite_sheet.get_height()
        animation_list = []

        for i in range(animation_steps):
            temp_img = sprite_sheet.subsurface(i * size, 0, size, size)
            animation_list.append(temp_img)

        return animation_list

    # so esta aqui pq eh chamado em play animation de forma especifica para cada filho
    def action(self, enemy_group):
        """
                Método de ação da torre. A ser implementado nas subclasses para ações específicas de cada tipo de torre.

                Args:
                - enemy_group: grupo de inimigos no jogo
        """
        pass

    # Realiza a animacao da torre dps ativa a sua acao, seja ela de dano ou dropar comida
    def play_animation(self, world, enemy_group):
        """
                Executa a animação da torre e, em seguida, sua ação.

                Args:
                - world: instância do mundo do jogo
                - enemy_group: grupo de inimigos no jogo
        """
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
        """
                Desenha a torre e sua área de alcance na tela.

                Args:
                - surface: superfície onde a torre será desenhada
        """
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    # Atualiza os dados da torre dps de um upgrade
    def upgrade(self):
        """
                Atualiza os dados da torre após um upgrade.
        """
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
        """
                Controla a habilidade especial da torre, se aplicável.
        """
        self.last_state_time = pg.time.get_ticks()
        self.cooldown_natural = self.cooldown
        self.pitbull_state = 1

    # same
    def pitbull_control(self, player, world):
        """
                Controla a habilidade especial da torre, se aplicável.

                Args:
                - player: instância do jogador no jogo
                - world: instância do mundo do jogo
        """
        if self.pitbull_state == 1:
            self.cooldown = self.cooldown_natural / c.PITBULL_FACTOR
            if pg.time.get_ticks() - self.last_state_time >= c.PITBULL_TIME / world.game_speed:
                self.last_state_time = pg.time.get_ticks()
                self.pitbull_state = 0
                self.cooldown = self.cooldown_natural

class TurretRancho(Turret):
    """
        Torre que dropa comida para o jogador.
    """
    def __init__(self, x, y):
        """
                Inicializa a torre Rancho com as coordenadas fornecidas.

                Args:
                - x, y: coordenadas da torre no jogo
        """
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
        """
                Cria um objeto de comida para a torre Rancho.
        """
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
        """
                Atualiza a torre Rancho a cada frame do jogo.

                Args:
                - enemy_group: grupo de inimigos no jogo
                - world: instância do mundo do jogo
        """
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
        """
                Desenha a torre Rancho e a comida, se houver, na tela.

                Args:
                - surface: superfície onde a torre e a comida serão desenhadas
        """
        super().draw(surface)
        if self.food is not None:
            self.food.draw(surface)

    # aplica os efeitos da comida no player
    def eat_food(self, player, mouse_pos):
        """
                Aplica os efeitos da comida no jogador, se clicada.

                Args:
                - player: instância do jogador no jogo
                - mouse_pos: posição do mouse na tela
        """
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
    """
        Torre que causa dano em área.
    """
    def __init__(self, x, y):
        """
                Inicializa a torre Aulão com as coordenadas fornecidas.

                Args:
                - x, y: coordenadas da torre no jogo
        """
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
        """
                Atualiza a torre Aulão a cada frame do jogo.

                Args:
                - enemy_group: grupo de inimigos no jogo
                - world: instância do mundo do jogo
        """
        # if target picked, play firing animation
        if pg.time.get_ticks() - self.last_action > (self.cooldown / world.game_speed) and self.target:
            self.play_animation(world, enemy_group)
        else:
            self.pick_target(enemy_group, world)
            self.boom.frame_index = 0
        self.pitbull_control(self, world)

    # faz a animacao da torre e do ataque
    def play_animation(self, world, enemy_group):
        """
                Desenha a torre Aulão e o ataque em área na tela.

                Args:
                - surface: superfície onde a torre e o ataque serão desenhados
        """
        super().play_animation(world, enemy_group)
        self.boom.update()

    # carrega os dados do sprite do ataque
    def load_boom(self):
        """
                Extrai imagens do spritesheet do ataque em área da torre Aulão.
        """
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
        """
                Cria um objeto de animação para o ataque em área da torre Aulão.
        """
        self.boom = Animation(self.x, self.y, self.boom_list)

    # desenha o a torre e o ataque
    def draw(self, surface):
        """
                Desenha a torre Aulão e o ataque em área na tela.

                Args:
                - surface: superfície onde a torre e o ataque serão desenhados
        """
        super().draw(surface)
        sprite_width = self.boom_list[0].get_width()
        if self.boom is not None:
            self.boom.draw(surface,self.x - sprite_width/2,self.y - sprite_width/2)

    # verifica se ha algum inimigo proximo
    def pick_target(self, enemy_group, world):
        """
                Verifica se há inimigos próximos para a torre Aulão atacar.

                Args:
                - enemy_group: grupo de inimigos no jogo
                - world: instância do mundo do jogo
        """
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
        """
                Ataca inimigos em área se houver algum próximo.
        Args:
            enemy_group:

        Returns:

        """
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
    """
        Torre que causa dano em um único alvo.
    """
    def __init__(self, x, y):
        """
                Inicializa a torre Gaga com as coordenadas fornecidas.

                Args:
                - x, y: coordenadas da torre no jogo
        """
        turret_spritesheets = []
        for i in range(1, c.TURRET_LEVELS + 1):
            turret_spritesheets.append(pg.image.load(f"./assets/turrets/TurretGaga/turret_{i}.png").convert_alpha())
        self.sprite_sheets = turret_spritesheets
        super().__init__(self.sprite_sheets, x, y, data.TURRET_GAGA_DATA)
        self.target = None

    # atualiza a cada frame do jogo
    def update(self, enemy_group, world):
        """
                Atualiza a torre Gaga a cada frame do jogo.

                Args:
                - enemy_group: grupo de inimigos no jogo
                - world: instância do mundo do jogo
        """
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
        """
                Verifica se há inimigos próximos para a torre Gaga atacar.

                Args:
                - enemy_group: grupo de inimigos no jogo
                - world: instância do mundo do jogo
        """
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
        """
                Ataca o primeiro alvo a entrar no alcance da torre Gaga.

                Args:
                - enemy_group: grupo de inimigos no jogo
        """
        if self.target:
            self.target.health -= self.damage
