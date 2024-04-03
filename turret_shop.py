import pygame as pg
from turret import Turret
from button import Button
from world import World
import constants as c


class TurretShop:
    """
     Uma classe que representa o shop de turrets, no caso, a loja do urubuzão.
     Essa classe também é responsável pela colocação das torres.
     Args:
         world_object: o objeto que representa o mundo

     Attributes:
     """
    def __init__(self, world_object):
        # Buttons:
        buy_turrent_image = pg.image.load("./assets/buttons/buy_turret.png").convert_alpha()
        cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()
        #individual turret image for mouse cursor
        self.cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()
        # Create buttons:
        self.turrent_button = Button(1030, 120, buy_turrent_image)
        self.cancel_button = Button(1030, 180, cancel_image)
        self.world = world_object
        self.placing_turrets = False

    def create_turret(self, mouse_pos, turret_group):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        turret = Turret(self.cursor_turret, mouse_tile_x, mouse_tile_y)
        turret_group.add(turret)

    def draw(self, surface):
        """
         Desenha a imagem do mundo numa superfície.
         Args:
             surface:

         """
        #draw buttons:
        if self.turrent_button.draw(surface):
            self.placing_turrets = True

        # if placing turrents then show the cancel button as well
        if self.placing_turrets:
            cursor_rect = self.cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDHT:
                surface.blit(self.cursor_turret, cursor_rect)
            if self.cancel_button.draw(surface) or pg.mouse.get_pressed()[2] == 1:
                self.placing_turrets = False
