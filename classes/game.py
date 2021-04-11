from classes.set_interval import set_timer
from classes.buttons import Button, Text
from classes.unit import Pet
from classes.global_vars import *
import pygame


class Game:
    def __init__(self):
        # screen initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Tamagotchi")
        self.screen = pygame.display.set_mode(DISPLAY)

        # pet initialization
        self.states = "bad"
        self.pet = Pet()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pet)

        self.best_score = self.pet.money

        # start menu objects
        self.button_start_game = Button((250, 310), MENU_BTN_SIZE, GRAY, YELLOW, text='PLAY', font_size=FONT_SIZE)
        self.button_exit = Button((250, 390), MENU_BTN_SIZE, GRAY, YELLOW, text='EXIT', font_size=FONT_SIZE)
        self.text_best_score = Text("Best score: {}$".format(self.best_score), (170, 230), YELLOW, font_size=35)
        self.logo = pygame.image.load("imgs/logo.png")
        self.logo = pygame.transform.scale(self.logo, (400, 100))

        self.start_objects = [self.button_start_game, self.button_exit, self.text_best_score]
        self.start_menu_show = True

        # game objects
        self.button_feed = Button((80, 100), BTN_SIZE, GRAY, PURPLE, text='Feed', font_size=FONT_SIZE)
        self.button_train = Button((190, 100), BTN_SIZE, GRAY, PURPLE, text='Train', font_size=FONT_SIZE)
        self.button_heal = Button((300, 100), BTN_SIZE, GRAY, PURPLE, text='Heal', font_size=FONT_SIZE)
        self.button_play = Button((410, 100), BTN_SIZE, GRAY, PURPLE, text='Play', font_size=FONT_SIZE)
        self.button_work = Button((370, 210), MENU_BTN_SIZE, GRAY, PURPLE, text='Work!', font_size=FONT_SIZE)
        self.button_list = [self.button_feed, self.button_train, self.button_heal, self.button_play, self.button_work]

        self.text_satiety = Text("satiety: {}".format(self.pet.satiety), (55, 400), RED)
        self.text_health = Text("health: {}".format(self.pet.health), (200, 400), RED)
        self.text_happiness = Text("happiness: {}".format(self.pet.happiness), (330, 400), RED)
        self.text_money = Text("Money: {}$".format(self.pet.money), (320, 290), YELLOW, font_size=30)
        self.text_list = [self.text_satiety, self.text_health, self.text_happiness, self.text_money]

        self.life_cycle_event = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_LIFE_CYCLE)
        self.interval_life_cycle = set_timer(self.life_cycle_event, 2, autostart=False)

        self.game_running = False

        # dead menu objects
        self.text_money_result = Text("Your pet have earned {} dollars".format(self.pet.money), (130, 50), BLACK)
        self.text_best_score2 = Text("Best score: {}$".format(self.best_score), (180, 85), YELLOW, font_size=30)
        self.button_restart_game = Button((250, 310), MENU_BTN_SIZE, GRAY, YELLOW, text='REPLAY', font_size=FONT_SIZE)
        self.button_menu = Button((250, 390), MENU_BTN_SIZE, GRAY, YELLOW, text='MENU', font_size=FONT_SIZE)
        self.grave = pygame.image.load("imgs/grave.png")
        self.grave = pygame.transform.scale(self.grave, (120, 120))

        self.dead_objects = [self.text_money_result, self.text_best_score2, self.button_restart_game, self.button_menu]
        self.dead_menu_show = False

    def start_menu(self):
        self.start_menu_show = True
        self.game_running = False
        self.dead_menu_show = False
        self.interval_life_cycle.stop()
        self.start_menu_loop()

    def start_game(self):
        self.pet.refresh_params()
        self.start_menu_show = False
        self.game_running = True
        self.dead_menu_show = False
        self.interval_life_cycle.start()
        self.game_loop()

    def dead_menu(self):
        self.start_menu_show = False
        self.game_running = False
        self.dead_menu_show = True
        self.interval_life_cycle.stop()
        self.dead_menu_loop()

    def game_ends(self):
        self.start_menu_show = False
        self.game_running = False
        self.dead_menu_show = False
        self.interval_life_cycle.stop()

    def check_victory(self, lose=0):
        if self.pet.satiety <= lose or self.pet.health <= lose:
            print("LOSE: ", self.pet.money)
            self.dead_menu()

    def game_loop(self):
        clock = pygame.time.Clock()
        while self.game_running:
            clock.tick(FPS)
            self.check_victory()

            for e in pygame.event.get():
                if e.type == pygame.USEREVENT:
                    if e.MyOwnType == ON_LIFE_CYCLE:
                        self.pet.life_cycle()
                        self.update_text()

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_a]:
                    self.pet.feed()

                elif pressed_keys[pygame.K_s]:
                    self.pet.train()

                elif pressed_keys[pygame.K_d]:
                    self.pet.heal()

                elif pressed_keys[pygame.K_k]:
                    self.pet.play()

                elif pressed_keys[pygame.K_l]:
                    self.pet.work()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_feed.rect.collidepoint(pos):
                            self.pet.feed()
                            self.button_feed.call_back()

                        elif self.button_train.rect.collidepoint(pos):
                            self.pet.train()
                            self.button_train.call_back()

                        elif self.button_heal.rect.collidepoint(pos):
                            self.pet.heal()
                            self.button_feed.call_back()

                        elif self.button_play.rect.collidepoint(pos):
                            self.pet.play()
                            self.button_feed.call_back()

                        elif self.button_work.rect.collidepoint(pos):
                            self.pet.work()
                            self.button_feed.call_back()

            self.update_text()
            self.pet.update_state()
            self.draw_everything()
            pygame.display.flip()

    def update_text(self):
        self.text_satiety.change_text("satiety: {}".format(self.pet.satiety))
        self.text_health.change_text("health: {}".format(self.pet.health))
        self.text_happiness.change_text("happiness: {}".format(self.pet.happiness))
        self.text_money.change_text("Money: {}$".format(self.pet.money))
        if self.pet.satiety >= 50:
            self.text_satiety.change_color(GREEN)
        elif self.pet.satiety >= 30:
            self.text_satiety.change_color(ORANGE)
        else:
            self.text_satiety.change_color(RED)

        if self.pet.health >= 50:
            self.text_health.change_color(GREEN)
        elif self.pet.health >= 30:
            self.text_health.change_color(ORANGE)
        else:
            self.text_health.change_color(RED)

        if self.pet.happiness >= 60:
            self.text_happiness.change_color(GREEN)
        elif self.pet.happiness >= 20:
            self.text_happiness.change_color(ORANGE)
        else:
            self.text_happiness.change_color(RED)

    def draw_everything(self):
        self.screen.fill(BACKGROUND_COLOR)
        for b in self.button_list:
            b.draw(self.screen)
        for t in self.text_list:
            t.draw(self.screen)
        self.all_sprites.draw(self.screen)

    def start_menu_loop(self):
        clock = pygame.time.Clock()
        while self.start_menu_show:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_RETURN]:
                    self.start_game()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_start_game.rect.collidepoint(pos):
                            self.start_game()
                        elif self.button_exit.rect.collidepoint(pos):
                            self.game_ends()

            self.screen.fill(BACKGROUND_COLOR)
            self.change_best_score()
            self.text_best_score.change_text("Best score: {}$".format(self.best_score))
            self.screen.blit(self.logo, (50, 95))
            for el in self.start_objects:
                el.draw(self.screen)
            pygame.display.flip()

    def dead_menu_loop(self):
        clock = pygame.time.Clock()
        while self.dead_menu_show:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_RETURN]:
                    self.start_game()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_restart_game.rect.collidepoint(pos):
                            self.start_game()
                        elif self.button_menu.rect.collidepoint(pos):
                            self.start_menu()

            self.screen.fill(BACKGROUND_COLOR)
            self.change_best_score()
            self.text_best_score2.change_text("Best score: {}$".format(self.best_score))
            self.text_money_result.change_text("Your pet have earned {} dollars".format(self.pet.money))
            self.screen.blit(self.grave, (185, 130))
            for el in self.dead_objects:
                el.draw(self.screen)
            pygame.display.flip()

    def change_best_score(self):
        if self.pet.money > self.best_score:
            self.best_score = self.pet.money
