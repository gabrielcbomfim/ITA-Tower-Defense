import pygame as pg


class Button():
    def __init__(self, x, y, image, visible=True, single_click=True):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.visible = visible
        self.single_click = single_click

    # desenha o botao na tela
    def draw(self, surface):
        if self.visible:
            # Draw button on screen
            surface.blit(self.image, self.rect)

    # verifica se o botao foi clicado
    def check_click(self, pos):
        action = False

        # Check mouseover and clicker conditions
        if self.rect.collidepoint(pos):
            if self.visible:
                action = True
                # If button is a single click type, set clicked to True
                if self.single_click:
                    self.visible = False

        return action
