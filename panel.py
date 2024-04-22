class Panel:
    def __init__(self, xrel, yrel, image, visible=True):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (xrel, yrel)
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            # Draw button on screen
            surface.blit(self.image, self.rect)