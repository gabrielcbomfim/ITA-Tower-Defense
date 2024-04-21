import pygame as pg
from turret import Turret
from button import Button
import constants as c


class Player:
    def __init__(self, turret_group, turret_spritesheets, world):
        self.placing_turrets = False
        self.selected_turret = None
        self.game_speed = 1

        self.health = c.HEALTH
        self.money = c.MONEY

        # individual turret image for mouse cursor
        cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()
        # Buttons images:
        upgrade_turret_image = pg.image.load("./assets/buttons/upgrade_turret.png").convert_alpha()
        cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()
        buy_turrent_image = pg.image.load("./assets/buttons/buy_turret.png").convert_alpha()
        begin_image = pg.image.load("./assets/buttons/begin.png").convert_alpha()
        restart_image = pg.image.load("./assets/buttons/restart.png").convert_alpha()
        fast_forward_image = pg.image.load("./assets/buttons/fast_forward.png").convert_alpha()

        # Create buttons:
        self.upgrade_button = Button(c.SCREEN_WIDHT + 5, 180, upgrade_turret_image)
        self.cancel_button = Button(c.SCREEN_WIDHT + 30, 180, cancel_image)
        self.turrent_button = Button(c.SCREEN_WIDHT + 30, 120, buy_turrent_image)
        self.begin_button = Button(c.SCREEN_WIDHT + 60, 300, begin_image)
        self.restart_button = Button(310, 300, restart_image)
        self.fast_forward_button = Button(c.SCREEN_WIDHT + 60, 340, fast_forward_image)

        self.cursor_turret = cursor_turret
        self.turret_group = turret_group
        self.turret_spritesheets = turret_spritesheets
        self.world = world

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        turret = Turret(self.turret_spritesheets, mouse_tile_x, mouse_tile_y)
        self.turret_group.add(turret)
        # deduct cost of turret
        self.money -= c.BUY_COST

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        for turret in self.turret_group:
            if abs(turret.tile_x - mouse_tile_x) <= 20 and abs(turret.tile_y - mouse_tile_y) <= 20:
                turret.selected = True
                return turret

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False

    def draw_ui(self, screen):
        # draw buttons:
        if self.turrent_button.draw(screen):
            self.placing_turrets = True
        # if placing turrents then show the cancel button as well
        if self.placing_turrets:
            cursor_rect = self.cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDHT:
                screen.blit(self.cursor_turret, cursor_rect)
            if self.cancel_button.draw(screen) or pg.mouse.get_pressed()[2] == 1:
                self.placing_turrets = False
        # if a turret is selected then show the upgrade button\
        if self.selected_turret:
            # if a turret is selected then show the upgrade button
            if self.selected_turret.upgrade_level < c.TURRET_LEVELS:
                if self.upgrade_button.draw(screen):
                    if self.money >= c.UPGRADE_COST:
                        self.money -= c.UPGRADE_COST
                        self.selected_turret.upgrade()

    def handle_input(self, event):
        # Check if is Mouse Click:
        if not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            return False
        mouse_pos = pg.mouse.get_pos()
        # Check if mouse is on the game area
        if mouse_pos[0] < c.SCREEN_WIDHT and mouse_pos[1] < c.SCREEN_HEIGHT:
            # clear selected turrets
            self.selected_turret = None
            self.clear_selection()

            if self.placing_turrets:
                if self.money >= c.BUY_COST:
                    self.create_turret(mouse_pos)
            else:
                self.selected_turret = self.select_turret(mouse_pos)
