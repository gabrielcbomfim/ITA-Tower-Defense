import pygame as pg


class World:
    """
     Uma classe que representa o mundo, no caso, o CTA.
     Args:
         map_image: A imagem png do mapa

     Attributes:
         image: A imagem do mapa.
     """
    def __init__(self,screen, data, map_image):
        self.paths = []
        self.level_data = data
        self.image = map_image
        self.x_ratio = screen.get_width()/(data['width']*data['tilewidth'])
        self.y_ratio = screen.get_height()/(data['height']*data['tileheight'])

    def process_data(self):
        """
        Olha para data para extrair informação relevante
        """
        for layer in self.level_data["layers"]:
            if "path" in layer["name"]:
                for obj in layer["objects"]:
                    self.process_waypoints(obj["polyline"], obj["x"], obj["y"])

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

