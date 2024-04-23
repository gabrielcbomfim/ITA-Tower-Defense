import pygame as pg
from enum import Enum
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA


class PlotStates(Enum):
    """
    Um enum que serve para abstrair o estados de um lote
    """
    FOR_SALE = 0
    FREE = 1
    OCCUPIED = 2


class Plot:
    """
    Uma classe que representa um lote onde vai ser colocado as torres
    Args:
        obj: O objeto do arquivo de dados do level json

    Attributes:
        x_left: Coordenada x do lado esquerdo
        x_right: Coordenada x do lado direito
        y_top: Coordenada y do lado de cima
        y_bottom: Coordenada y do lado de baixo
        state: Estado do lote (FOR_SALE, FREE, OCCUPIED)
    """

    def __init__(self, obj, x_ratio, y_ratio):
        self.x_left = obj['x'] * x_ratio
        self.x_right = (obj['x'] + obj['width']) * x_ratio
        self.y_top = obj['y'] * y_ratio
        self.y_bottom = (obj['y'] + obj['height']) * y_ratio
        self.state = PlotStates.FOR_SALE

    def is_in(self, pos):
        return self.x_left <= pos[0] <= self.x_right and self.y_top <= pos[1] <= self.y_bottom

    def center(self):
        return (self.x_left + self.x_right) / 2, (self.y_top + self.y_bottom) / 2


class World:
    """
     Uma classe que representa o mundo, no caso, o CTA.
     Args:
         map_image: A imagem png do mapa

     Attributes:
         image: A imagem do mapa.
     """

    def __init__(self, screen, data, map_image):
        self.game_over = False
        self.game_outcome = 0  # -1 is loss, 1 is win
        self.level_started = False
        self.level = 3
        self.game_speed = c.GAME_SPEED
        self.paths = []
        self.plots = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.last_enemy_spawn = pg.time.get_ticks()
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

        self.x_ratio = screen.get_width() / (data['width'] * data['tilewidth'])
        self.y_ratio = screen.get_height() / (data['height'] * data['tileheight'])

    def process_data(self):
        """
        Olha para data para extrair informação relevante
        """
        for layer in self.level_data["layers"]:
            if "path" in layer["name"]:
                for obj in layer["objects"]:
                    self.process_waypoints(obj["polyline"], obj["x"], obj["y"])
            elif "lote" in layer["name"]:
                for obj in layer["objects"]:
                    # Armazena as posições corrigidas dos lotes:
                    self.plots.append(Plot(obj, self.x_ratio, self.y_ratio))

    def process_waypoints(self, points, abs_x, abs_y):
        """
        Itera pelos waypoints para extrair sets individuais das coordenadas x e y
        Args:
         points: Lista de dicionários de coordenadas x e y
         abs_x: x absoluto (x do primeiro ponto)
         abs_y: y absoluto (y do primeiro ponto)
        """
        waypoints = []
        for point in points:
            temp_x = (abs_x + point.get("x")) * self.x_ratio
            temp_y = (abs_y + point.get("y")) * self.y_ratio
            waypoints.append((temp_x, temp_y))
        self.paths.append(waypoints)

    def draw(self, surface):
        """
         Desenha a imagem do mundo numa superfície.
         Args:
             surface:

         """
        surface.blit(self.image, (0, 0))

    def process_enemies(self):
        """
        Processa os inimigos do arquivo de dados
        """
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        # now randomize the list to shuffle the enemies
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        """
        Checa se o level foi completado
        """
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_level(self):
        """
        Reseta o level
        """
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.enemy_list = []
