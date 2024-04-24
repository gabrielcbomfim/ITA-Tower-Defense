import pygame as pg
import turret as Turrets
import turret_data
from button import Button
from world import PlotStates
from panel import Panel
from enum import Enum
from animation import Animation
import math
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
        self.range_image = None
        self.range_rect = None

        self.i_count = 0
        self.i_list = []
        self.money = c.MONEY

        # Saude para
        self.max_health = 100
        self.health = 100

        # load fonts for text on screen
        self.small_font = pg.font.SysFont("Consolas", 20, bold = True)
        self.text_font = pg.font.SysFont("Consolas", 36, bold=True)
        self.large_font = pg.font.SysFont("Consolas", 108)

        # Load Sounds:
        self.viradao_sound = pg.mixer.Sound("assets/audio/Efeito_sonoro_viradao.wav")
        self.G_audio = pg.mixer.Sound("assets/audio/G_loko_audio.wav")
        self.bomba_audio = pg.mixer.Sound("assets/audio/Audio_Explosao.wav")
        self.eating_audio = pg.mixer.Sound("assets/audio/Audio_Pou_Comendo.wav")
        # Preview Cursor Images:
        self.cursor_turret = pg.image.load("./assets/turrets/cursor_gaga.png").convert_alpha()
        self.cursor_turret = pg.transform.scale(self.cursor_turret, (60, 60))
        self.cursor_rancho = pg.image.load("./assets/turrets/cursor_rancho.png").convert_alpha()
        self.cursor_bomba = pg.image.load("./assets/abilities/bomba.png").convert_alpha()
        self.cursor_G = pg.image.load("./assets/abilities/G.png").convert_alpha()
        self.cursor_pitbull = pg.image.load('./assets/abilities/pitbull.png').convert_alpha()
        self.g_image_spritesheet = pg.image.load("./assets/abilities/G_spritesheet.png").convert_alpha()
        self.g_image_spritesheet  = pg.transform.scale(self.g_image_spritesheet, (480, 120))

        # Panel image:
        panel_image = pg.image.load("./assets/buttons/panel_image.png").convert_alpha()

        # I image:
        self.i_image = pg.image.load("./assets/buttons/I.png").convert_alpha()

        # Buttons images:
        upgrade_turret_image = pg.image.load("./assets/buttons/upgrade_turret.png").convert_alpha()
        cancel_image = pg.image.load("./assets/buttons/cancel.png").convert_alpha()
        begin_image = pg.image.load("./assets/buttons/begin.png").convert_alpha()
        restart_image = pg.image.load("./assets/buttons/restart.png").convert_alpha()
        fast_forward_image = pg.image.load("./assets/buttons/fast_forward.png").convert_alpha()
        # Turrets images:
        torre_gaga_image = pg.image.load("./assets/turrets/TurretGaga/gaga_icone.png").convert_alpha()
        torre_aulao_image = pg.image.load("./assets/turrets/TurretAulao/aulao_icone.png").convert_alpha()
        torre_rancho_image = pg.image.load("./assets/turrets/TurretRancho/turret_3.png").convert_alpha()
        torre_rancho_image = pg.transform.scale(torre_rancho_image, (110, 110))
        # Abilities images:
        viradao_image = pg.image.load("./assets/buttons/viradao_icone.png").convert_alpha()
        viradao_image = pg.transform.scale(viradao_image, (120, 120))
        g_image = pg.image.load("./assets/buttons/G_icone.png").convert_alpha()
        g_image = pg.transform.scale(g_image, (120, 120))
        pitbull_image = pg.image.load("./assets/buttons/Pitbull_moldura.png").convert_alpha()
        pitbull_image = pg.transform.scale(pitbull_image, (120, 120))
        bomba_image = pg.image.load("./assets/buttons/bomba_icone.png").convert_alpha()
        bomba_image = pg.transform.scale(bomba_image, (120, 120))

        # Create panel:
        self.panel = Panel(c.SCREEN_WIDHT - 140, 0, panel_image)

        # Create buttons:
        self.upgrade_button = Button(c.SCREEN_WIDHT + 230, 760, upgrade_turret_image, False)
        self.cancel_button = Button(c.SCREEN_WIDHT + 230, 820, cancel_image, False)
        self.begin_button = Button(c.SCREEN_WIDHT + 30, 760, begin_image)
        self.restart_button = Button(c.SCREEN_WIDHT + 30, 880, restart_image, True)
        self.fast_forward_button = Button(c.SCREEN_WIDHT + 30, 820, fast_forward_image, True, False)
        # Turret buttons:
        self.gaga_button = Button(c.SCREEN_WIDHT + 210, 150, torre_gaga_image, True, False)
        self.aulao_button = Button(c.SCREEN_WIDHT + 330, 150, torre_aulao_image, True, False)
        self.rancho_button = Button(c.SCREEN_WIDHT + 50, 140, torre_rancho_image, True, False)
        #Abilities buttons
        self.viradao_button = Button(c.SCREEN_WIDHT + 240, 420, viradao_image, True, False)
        self.g_button = Button(c.SCREEN_WIDHT + 20, 420, g_image, True, False)
        self.pitbull_button = Button(c.SCREEN_WIDHT + 20, 280, pitbull_image, True, False)
        self.bomba_button = Button(c.SCREEN_WIDHT + 240, 280, bomba_image, True, False)

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
        draw_text(screen, "Saúde: "+str(self.health)+"/"+str(self.max_health), self.text_font, "red",  c.SCREEN_WIDHT+30, 680)
        if self.world.level == 11:
            draw_text(screen, "INFERNINHO", self.text_font, "red", c.SCREEN_WIDHT + 30, 720)
        else:
            draw_text(screen, "Semestre: "+str(self.world.level), self.text_font, "grey100",  c.SCREEN_WIDHT+30, 720)

        # Draw description texts:
        draw_text(screen, "Gagá-" + str(turret_data.TURRET_GAGA_DATA[0]["buy_cost"]) + "B", self.small_font,
                  "darkgreen", c.SCREEN_WIDHT+210, 250)
        draw_text(screen, "Aulão-" + str(turret_data.TURRET_AULAO_DATA[0]["buy_cost"]) + "B", self.small_font,
                  "darkgreen", c.SCREEN_WIDHT+330, 250)
        draw_text(screen, "Rancho-" + str(turret_data.TURRET_RANCHO_DATA[0]["buy_cost"]) + "B", self.small_font,
                  "darkgreen", c.SCREEN_WIDHT + 50, 250)
        # Descriptions for the abilities:
        draw_text(screen, "G", self.text_font, "black",  c.SCREEN_WIDHT + 150, 430)
        draw_text(screen, "Empurra", self.small_font, "black", c.SCREEN_WIDHT + 150, 470)
        draw_text(screen, str(c.G_CUSTO) + " Saúde", self.small_font, "darkred", c.SCREEN_WIDHT + 150, 500)

        draw_text(screen, "Viradão", self.small_font, "black", c.SCREEN_WIDHT + 370, 430)
        draw_text(screen, "+Tempo", self.small_font, "black", c.SCREEN_WIDHT + 370, 470)
        draw_text(screen, str(100* c.VIRADAO_VIDA_PROPORCIONAL) + "% da", self.small_font, "darkred", c.SCREEN_WIDHT + 370, 500)
        draw_text(screen, "Saúde Max", self.small_font, "darkred", c.SCREEN_WIDHT + 370, 530)

        draw_text(screen, "Bomba", self.small_font, "black", c.SCREEN_WIDHT + 370, 290)
        draw_text(screen, str(c.BOMBA_DANO) + " de dano", self.small_font, "black", c.SCREEN_WIDHT + 370, 320)
        draw_text(screen, str(c.BOMBA_CUSTO_BIZUS) + " Bizus", self.small_font, "darkgreen", c.SCREEN_WIDHT + 370,350)
        draw_text(screen, str(c.BOMBA_CUSTO_SAUDE) + " Saúde", self.small_font, "darkred", c.SCREEN_WIDHT + 370, 380)

        draw_text(screen, "Pitbull", self.small_font, "black", c.SCREEN_WIDHT + 150, 290)
        draw_text(screen, "+Veloz", self.small_font, "black", c.SCREEN_WIDHT + 150, 320)
        draw_text(screen, str(c.PITBULL_CUSTO_BIZUS) + " Bizus", self.small_font, "darkgreen", c.SCREEN_WIDHT + 150, 350)
        draw_text(screen, str(c.PITBULL_CUSTO_SAUDE) + " Saúde", self.small_font, "darkred", c.SCREEN_WIDHT + 150, 380)

        # draw buttons:
        self.upgrade_button.draw(screen)
        self.cancel_button.draw(screen)
        self.begin_button.draw(screen)
        self.restart_button.draw(screen)
        self.fast_forward_button.draw(screen)
        # Turret buttons:
        self.aulao_button.draw(screen)
        self.gaga_button.draw(screen)
        self.rancho_button.draw(screen)
        #Abilities buttons:
        self.viradao_button.draw(screen)
        self.g_button.draw(screen)
        self.pitbull_button.draw(screen)
        self.bomba_button.draw(screen)

        # if placing turrets then show turret preview
        if self.placing_state != PlacingStates.NOT_PLACING:

            # Escolha do cursor preview:
            switch_case_cursor = {
                PlacingStates.TORRE_AULAO: self.cursor_turret,
                PlacingStates.TORRE_RANCHO: self.cursor_rancho,
                PlacingStates.TORRE_DO_GAGA: self.cursor_turret,
                PlacingStates.G: self.cursor_G,
                PlacingStates.BOMBA: self.cursor_bomba,
                PlacingStates.PITBULL: self.cursor_pitbull
            }
            cursor_preview = switch_case_cursor[self.placing_state]
            cursor_rect = cursor_preview.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDHT:
                # Se for G ou bomba botar circulo:
                if self.placing_state == PlacingStates.G:
                    radius = c.G_RADIUS
                elif self.placing_state == PlacingStates.BOMBA:
                    radius = c.BOMBA_RADIUS
                elif self.placing_state == PlacingStates.PITBULL:
                    radius = c.PITBULL_RADIUS

                if self.placing_state in [PlacingStates.G, PlacingStates.BOMBA, PlacingStates.PITBULL]:
                    self.range_image = pg.Surface((radius * 2, radius * 2))
                    self.range_image.fill((0, 0, 0))
                    self.range_image.set_colorkey((0, 0, 0))
                    pg.draw.circle(self.range_image, "grey100", (radius,  radius), radius)
                    self.range_image.set_alpha(50)
                    self.range_rect = self.range_image.get_rect()
                    self.range_rect.center = (cursor_pos[0], cursor_pos[1])
                    screen.blit(self.range_image, self.range_rect)

                # Por fim desenhar o icone:
                screen.blit(cursor_preview, cursor_rect)

        if self.world.game_over:
            # pg.draw.rect(screen, "black", (200, 200, 1000, 400), border_radius=30)
            if self.world.game_outcome == -1:
                # Carregue a imagem original
                end_image = pg.image.load("./assets/mapa/desligado.png").convert_alpha()

                # Aumente o tamanho da imagem por 5 vezes
                end_image = pg.transform.scale(end_image, (end_image.get_width() * 5, end_image.get_height() * 5))

                # Exiba a imagem no centro da tela
                screen.blit(end_image, ((screen.get_width() - end_image.get_width()) // 2, (screen.get_height() - end_image.get_height()) // 2))

            elif self.world.game_outcome == 1:
                # Carregue a imagem original
                end_image = pg.image.load("./assets/mapa/voce formou.png").convert_alpha()

                # Aumente o tamanho da imagem por 5 vezes
                end_image = pg.transform.scale(end_image, (end_image.get_width() * 5, end_image.get_height() * 5))

                # Exiba a imagem no centro da tela
                screen.blit(end_image, (
                (screen.get_width() - end_image.get_width()) // 2, (screen.get_height() - end_image.get_height()) // 2))


    # Returns true if click has resulted in a successful action
    def handle_input(self, event, screen):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.placing_state = PlacingStates.NOT_PLACING
            self.cancel_button.visible = False
            self.upgrade_button.visible = False
            self.selected_turret = None
            self.clear_selection()
            return True

        # Check if event is Mouse Click:
        if not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            return False

        mouse_pos = pg.mouse.get_pos()

        # Towers:

        if self.rancho_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.TORRE_RANCHO
            return True

        if self.gaga_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.TORRE_DO_GAGA
            return True

        if self.aulao_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.TORRE_AULAO

        # Abilities:
        if self.viradao_button.check_click(mouse_pos) and self.run and self.viradao_state == 0 and self.health > 0:
            self.viradao_state = 1
            self.viradao_sound.play()
            self.last_state_time = pg.time.get_ticks()
            self.change_health(-(c.VIRADAO_VIDA_PROPORCIONAL * self.max_health))
            for enemy in self.enemy_group:
                enemy.viradao()
            return True

        if self.g_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.G
            return True

        if self.bomba_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.BOMBA
            return True

        if self.pitbull_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.PITBULL
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
            pg.mixer.music.load('assets/audio/CovaDela90BPM.wav')
            pg.mixer.music.play(-1)
            self.restart = True
            self.run = False
            return True

        if self.upgrade_button.check_click(mouse_pos):
            if self.money >= c.UPGRADE_COST:
                self.money -= c.UPGRADE_COST
                self.selected_turret.upgrade()
                return True

        if self.cancel_button.check_click(mouse_pos):
            self.placing_state = PlacingStates.NOT_PLACING
            self.cancel_button.visible = False
            self.upgrade_button.visible = False
            self.selected_turret = None
            self.clear_selection()
            return True

        for turret in self.turret_group:
            if type(turret) is Turrets.TurretRancho and True:
                if turret.eat_food(self, mouse_pos):
                    self.eating_audio.play()
                    return True

        # Put the turret or ability:
        # Check if mouse is on the game area:
        if mouse_pos[0] < c.SCREEN_WIDHT and mouse_pos[1] < c.SCREEN_HEIGHT:
            # clear selected turrets
            self.selected_turret = None
            self.clear_selection()

            # Se bota G:
            if self.placing_state == PlacingStates.G and self.health > 0:
                self.G_audio.play()
                self.health -= c.G_CUSTO
                ## G:

                g_animation = Animation(mouse_pos[0],mouse_pos[1],[self.g_image_spritesheet])
                g_animation.image = self.g_image_spritesheet
                g_animation.load_image(4)
                g_animation.frame_index = 0
                g_animation.draw_instant(screen, mouse_pos[0], mouse_pos[1])

                for enemy in self.enemy_group:
                    if pg.math.Vector2(mouse_pos).distance_to(enemy.pos) < c.G_RADIUS:
                        enemy.g()

            # Se bota Pitbull:
            if self.placing_state == PlacingStates.PITBULL and self.health > 0 and (self.money - c.PITBULL_CUSTO_BIZUS) >=0:
                self.health -= c.PITBULL_CUSTO_SAUDE
                self.money -= c.PITBULL_CUSTO_BIZUS
                for turret in self.turret_group:
                    if pg.math.Vector2(mouse_pos).distance_to(pg.math.Vector2(turret.x, turret.y)) < c.PITBULL_RADIUS:
                        turret.pitbull()

            # Se bota bomba:
            if self.placing_state == PlacingStates.BOMBA and self.health > 0 and (self.money - c.BOMBA_CUSTO_BIZUS) >=0:
                self.health -= c.BOMBA_CUSTO_SAUDE
                self.money -= c.BOMBA_CUSTO_BIZUS
                self.bomba_audio.play()
                for enemy in self.enemy_group:
                    if pg.math.Vector2(mouse_pos).distance_to(enemy.pos) < c.BOMBA_RADIUS:
                        enemy.bomba()

            # Se torre:
            if self.placing_state in [PlacingStates.TORRE_RANCHO, PlacingStates.TORRE_AULAO, PlacingStates.TORRE_DO_GAGA]:
                if self.create_turret(mouse_pos):
                    return True
            else:
                self.selected_turret = self.select_turret(mouse_pos)
                if self.selected_turret is not None:
                    self.placing_state = PlacingStates.NOT_PLACING
                    return True

        return False


