class Panel:
    def __init__(self, x, y, image, visible=True):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            # Draw button on screen
            surface.blit(self.image, self.rect)