import json
import pygame as pg
from turret import Turret
import constants as c


class Player:
    def __init__(self, upgrade_button, cancel_button, turret_button,
                 cursor_turret, turret_group, turret_spritesheets, world):
        self.placing_turrets = False
        self.selected_turret = None
        self.game_speed = 1

        self.health = c.HEALTH
        self.money = c.MONEY

        self.upgrade_button = upgrade_button
        self.cancel_button = cancel_button
        self.cursor_turret = cursor_turret
        self.turrent_button = turret_button
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
