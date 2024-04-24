import pygame as pg
import turret as Turrets
from button import Button
from world import PlotStates
from panel import Panel
from enum import Enum
import constants as c


# function for outputting text on screen
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class PlacingStates(Enum):
    """
    Um enum que serve para abstrair o estados de colocar coisas (habilidades e torres)
    """
    NOT_PLACING = 0
    TORRE_DO_GAGA = 1
    TORRE_AULAO = 2
    TORRE_RANCHO = 3
    BOMBA = 4
    G = 5
    VIRADAO = 6
    PITBULL = 7


class Player:
    def __init__(self, turret_group, world, enemy_group):
        # Incializar o estado de placing como estado neutro:
        self.placing_state = PlacingStates.NOT_PLACING
        self.selected_turret = None
        self.restart = True
        self.run = True
        self.enemy_group = enemy_group

        #Controle de habilidades:
        self.viradao_state = 0
        self.last_state_time = pg.time.get_ticks()

        self.i_count = 0
        self.i_list = []
        self.money = c.MONEY

        # Saude para
        self.max_health = 100
        self.health = 100

        # load fonts for text on screen
        self.text_font = pg.font.SysFont("Consolas", 36, bold=True)
        self.large_font = pg.font.SysFont("Consolas", 48)

        # Load Sounds:
        self.viradao_sound = pg.mixer.Sound("assets/audio/Efeito_sonoro_viradao.wav")

        # Preview Cursor Images:
        self.cursor_turret = pg.image.load("./assets/turrets/cursor_turret.png").convert_alpha()
        self.cursor_bomba = pg.image.load("./assets/abilities/bomba.png").convert_alpha()
        self.cursor_G = pg.image.load("./assets/abilities/G.png").convert_alpha()
        self.cursor_pitbull = pg.image.load('./assets/abilities/pitbull.png').convert_alpha()

        # Panel image:
        panel_image = pg.image.load("./assets/buttons/panel_image.png").convert_alpha()

        # I image:
        self.i_image = pg.image.load("./assets/buttons/I.png").convert_alpha()

        # Buttons images:
        upgrade_turret_image = pg.image.load("./assets/buttons/upgrade_turret.png").convert_alpha()
        cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()
        buy_turrent_image = pg.image.load("./assets/buttons/buy_turret.png").convert_alpha()
        begin_image = pg.image.load("./assets/buttons/begin.png").convert_alpha()
        restart_image = pg.image.load("./assets/buttons/restart.png").convert_alpha()
        fast_forward_image = pg.image.load("./assets/buttons/fast_forward.png").convert_alpha()

        # Abilities images:
        viradao_image = pg.image.load("./assets/buttons/viradao_icone.png").convert_alpha()
        viradao_image = pg.transform.scale(viradao_image, (140, 140))

        # Create panel:
        self.panel = Panel(c.SCREEN_WIDHT - 140, 0, panel_image)

        # Create buttons:
        self.upgrade_button = Button(c.SCREEN_WIDHT + 230, 760, upgrade_turret_image, False)
        self.cancel_button = Button(c.SCREEN_WIDHT + 230, 820, cancel_image, False)
        self.turrent_button = Button(c.SCREEN_WIDHT + 30, 120, buy_turrent_image, True, False)
        self.begin_button = Button(c.SCREEN_WIDHT + 30, 760, begin_image)
        self.restart_button = Button(310, 420, restart_image, False)
        self.fast_forward_button = Button(c.SCREEN_WIDHT + 30, 820, fast_forward_image, True, False)

        #Abilities buttons
        self.viradao_button = Button(c.SCREEN_WIDHT + 300, 400, viradao_image, True, False)

        self.turret_group = turret_group
        self.world = world

    def change_health(self, delta_health):
        self.health += delta_health
        self.health = min(self.health, self.max_health)

    def create_turret(self, mouse_pos):
        for plot in self.world.plots:
            if plot.state == PlotStates.FOR_SALE and plot.is_in(mouse_pos):
                if self.placing_state == PlacingStates.TORRE_AULAO:
                    turret = Turrets.TurretAulao(plot.center()[0], plot.center()[1])
                elif self.placing_state == PlacingStates.TORRE_DO_GAGA:
                    turret = Turrets.TurretGaga(plot.center()[0], plot.center()[1])
                elif self.placing_state == PlacingStates.TORRE_RANCHO:
                    turret = Turrets.TurretRancho(plot.center()[0], plot.center()[1])
                else:
                    return False

                if self.money >= turret.buy_cost:
                    self.turret_group.add(turret)
                    # deduct cost of turret
                    self.money -= c.BUY_COST
                    plot.state = PlotStates.OCCUPIED
                    return True
                else:
                    return False
        return False

    def select_turret(self, mouse_pos):
        for turret in self.turret_group:
            if abs(turret.x - mouse_pos[0]) <= 20 and abs(turret.y - mouse_pos[1]) <= 20:
                turret.selected = True
                return turret

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False
            self.upgrade_button.visible = False

    def update(self, world):
        # Abilities Control:
        if self.viradao_state == 1:
            if (pg.time.get_ticks() - self.last_state_time >=
                    (c.VIRADAO_TIME_1 + c.VIRADAO_TIME_2 + c.VIRADAO_TIME_3)/world.game_speed):
                self.viradao_state = 0

        # highlight selected turret
        if self.selected_turret:
            self.selected_turret.selected = True

        if self.placing_state != PlacingStates.NOT_PLACING:
            self.cancel_button.visible = True

        if self.world.game_over:
            # restart button
            self.restart_button.visible = True
        else:
            # check if the level started or not
            if not self.world.level_started:
                self.begin_button.visible = True

        # if a turret is selected then show the upgrade button\
        if self.selected_turret:
            # if a turret is selected then show the upgrade button
            if self.selected_turret.upgrade_level < c.TURRET_LEVELS:
                self.upgrade_button.visible = True

    def add_i(self):
        self.i_count += 1
        self.max_health -= 15
        self.change_health(0)


    def draw_i(self, screen):
        for i in range(min(self.i_count, c.I_LIMIT)):
            i_rect = self.i_image.get_rect()
            i_rect.topleft = (c.SCREEN_WIDHT + 80 * i + 20, 930)
            screen.blit(self.i_image, i_rect)


    def draw_ui(self, screen):
        # draw panel:
        self.panel.draw(screen)

        # draw text:
        self.draw_i(screen)
        draw_text(screen, "Bizus: "+str(self.money), self.text_font, "green", c.SCREEN_WIDHT+30, 640)
        draw_text(screen, "Saúde: "+str(self.health)+"/"+str(self.max_health), self.text_font, "darkred",  c.SCREEN_WIDHT+30, 680)
        draw_text(screen, "Semestre: "+str(self.world.level), self.text_font, "grey100",  c.SCREEN_WIDHT+30, 720)

        # draw buttons:
        self.upgrade_button.draw(screen)
        self.cancel_button.draw(screen)
        self.turrent_button.draw(screen)
        self.begin_button.draw(screen)
        self.restart_button.draw(screen)
        self.fast_forward_button.draw(screen)
        #Abilities buttons:
        self.viradao_button.draw(screen)

        # if placing turrents then show turret preview
        if self.placing_state != PlacingStates.NOT_PLACING:
            cursor_rect = self.cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos

            # Escolha do cursor preview:
            switch_case_cursor = {
                PlacingStates.TORRE_AULAO: self.cursor_turret,
                PlacingStates.TORRE_RANCHO: self.cursor_turret,
                PlacingStates.TORRE_DO_GAGA: self.cursor_turret,
                PlacingStates.G: self.cursor_G,
                PlacingStates.BOMBA: self.cursor_bomba,
                PlacingStates.PITBULL: self.cursor_pitbull
            }
            cursor_preview = switch_case_cursor[self.placing_state]
            if cursor_pos[0] <= c.SCREEN_WIDHT:
                screen.blit(cursor_preview, cursor_rect)

        if self.world.game_over:
            pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
            if self.world.game_outcome == -1:
                draw_text(screen, "GAME OVER", self.large_font, "grey100", 310, 250)
            elif self.world.game_outcome == 1:
                draw_text(screen, "YOU WIN", self.large_font, "grey100", 315, 250)

    # Returns true if click has resulted in a successful action
    def handle_input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.placing_state = PlacingStates.NOT_PLACING
            return True

        # Check if event is Mouse Click:
        if not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            return False

        mouse_pos = pg.mouse.get_pos()

        # Towers:
        #Todo: Depois mudar esse botão turret para alguma torre especifica por exemplo aulao:
        if self.turrent_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.TORRE_AULAO
            return True

        # Abilities:

        if self.viradao_button.check_click(mouse_pos) and self.run and self.viradao_state == 0:
            self.viradao_state = 1
            self.viradao_sound.play()
            self.change_health(-(c.VIRADAO_VIDA_PROPORCIONAL * self.max_health))
            for enemy in self.enemy_group:
                enemy.viradao()
            return True

        if self.begin_button.check_click(mouse_pos):
            self.world.level_started = True
            # Tocar musica agitada:
            pg.mixer.music.load('assets/audio/CovaDela180BPM.wav')
            pg.mixer.music.play(-1)
            return True

        if self.fast_forward_button.check_click(mouse_pos):
            if self.world.game_speed == 1:
                self.world.game_speed = 2
            else:
                self.world.game_speed = 1
            return True

        if self.restart_button.check_click(mouse_pos):
            self.restart = True
            self.run = False
            return True

        if self.upgrade_button.check_click(mouse_pos):
            if self.money >= c.UPGRADE_COST:
                self.money -= c.UPGRADE_COST
                self.selected_turret.upgrade()
                return True

        if self.cancel_button.check_click(mouse_pos) or pg.mouse.get_pressed()[2] == 1:
            self.placing_state = PlacingStates.NOT_PLACING
            return True

        for turret in self.turret_group:
            if type(turret) is Turrets.TurretRancho and True:
                if turret.eat_food(self, mouse_pos):
                    return True

        # Check if mouse is on the game area
        if mouse_pos[0] < c.SCREEN_WIDHT and mouse_pos[1] < c.SCREEN_HEIGHT:
            # clear selected turrets
            self.selected_turret = None
            self.clear_selection()

            if self.create_turret(mouse_pos):
                return True
            else:
                self.selected_turret = self.select_turret(mouse_pos)
                if self.selected_turret is not None:
                    return True

        return False
