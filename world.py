import pygame as pg


class World:
    """
     Uma classe que representa o mundo, no caso, o CTA.
     Args:
         map_image: A imagem png do mapa

     Attributes:
         image: A imagem do mapa.
     """
    def __init__(self, map_image):
        self.image = map_image

    def draw(self, surface):
        """
         Desenha a imagem do mundo numa superfície.
         Args:
             surface:

         """
        surface.blit(self.image, (0, 0))