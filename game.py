from set_interval import *
from buttons import *
from unit import *


class Game:
    def __init__(self):
        # screen initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Tamagotchi")
        self.screen = pygame.display.set_mode(DISPLAY)

        # start menu objects
        self.button_start_game = Button((250, 290), MENU_BTN_SIZE, GRAY, YELLOW, text='PLAY', font_size=FONT_SIZE)
        self.button_exit = Button((250, 370), MENU_BTN_SIZE, GRAY, YELLOW, text='EXIT', font_size=FONT_SIZE)
        self.logo = pygame.image.load("imgs/logo.png")
        self.logo = pygame.transform.scale(self.logo, (400, 100))

        self.start_menu_show = True

        # pet initialization
        self.states = "bad"
        self.pet = Pet()

        # game objects
        self.button_feed = Button((80, 100), BTN_SIZE, GRAY, PURPLE, text='Feed', font_size=FONT_SIZE)
        self.button_train = Button((190, 100), BTN_SIZE, GRAY, PURPLE, text='Train', font_size=FONT_SIZE)
        self.button_heal = Button((300, 100), BTN_SIZE, GRAY, PURPLE, text='Heal', font_size=FONT_SIZE)
        self.button_play = Button((410, 100), BTN_SIZE, GRAY, PURPLE, text='Play', font_size=FONT_SIZE)
        self.button_list = [self.button_feed, self.button_train, self.button_heal, self.button_play]

        self.text_satiety = Text("satiety: {}".format(self.pet.satiety), (55, 400), (255, 0, 0))
        self.text_health = Text("health: {}".format(self.pet.health), (200, 400), (255, 0, 0))
        self.text_happiness = Text("happiness: {}".format(self.pet.happiness), (330, 400), (255, 0, 0))
        self.text_list = [self.text_satiety, self.text_health, self.text_happiness]

        self.life_cycle_event = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_LIFE_CYCLE)
        self.interval_life_cycle = set_timer(self.life_cycle_event, 2, autostart=False)

        self.game_running = False

        # dead menu objects
        self.text_money_result = Text("Your pet have earned {} dollars".format(self.pet.money), (130, 60), BLACK)
        self.button_restart_game = Button((250, 300), MENU_BTN_SIZE, GRAY, YELLOW, text='REPLAY', font_size=FONT_SIZE)
        self.button_exit2 = Button((250, 380), MENU_BTN_SIZE, GRAY, YELLOW, text='EXIT', font_size=FONT_SIZE)
        self.grave = pygame.image.load("imgs/grave.png")
        self.grave = pygame.transform.scale(self.grave, (125, 125))

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

    def check_victory(self, lose=0, win=100):
        if self.pet.satiety <= lose or self.pet.health <= lose:
            print("LOSE")
            self.dead_menu()
        elif self.pet.satiety >= win and self.pet.health >= win\
                and self.pet.happiness >= win:
            print("WIN")
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

                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_a]:
                    self.pet.feeding()

                elif pressed_keys[K_s]:
                    self.pet.training()

                elif pressed_keys[K_d]:
                    self.pet.healing()

                elif pressed_keys[K_f]:
                    self.pet.playing()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_feed.rect.collidepoint(pos):
                            self.pet.feeding()
                            self.button_feed.call_back()

                        elif self.button_train.rect.collidepoint(pos):
                            self.pet.training()
                            self.button_train.call_back()

                        elif self.button_heal.rect.collidepoint(pos):
                            self.pet.healing()
                            self.button_feed.call_back()

                        elif self.button_play.rect.collidepoint(pos):
                            self.pet.playing()
                            self.button_feed.call_back()

            self.update_text()
            self.pet.update_state()
            self.draw_everything()
            pygame.display.flip()

    def update_text(self):
        self.text_satiety.change_text("satiety: {}".format(self.pet.satiety))
        self.text_health.change_text("health: {}".format(self.pet.health))
        self.text_happiness.change_text("happiness: {}".format(self.pet.happiness))

    def draw_everything(self):
        self.screen.fill(BACKGROUND_COLOR)
        for b in self.button_list:
            b.draw(self.screen)
        for t in self.text_list:
            t.draw(self.screen)
        self.pet.draw(self.screen)

    def start_menu_loop(self):
        clock = pygame.time.Clock()
        while self.start_menu_show:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_start_game.rect.collidepoint(pos):
                            self.start_game()
                        elif self.button_exit.rect.collidepoint(pos):
                            self.game_ends()

            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.logo, (50, 120))
            self.button_start_game.draw(self.screen)
            self.button_exit.draw(self.screen)
            pygame.display.flip()

    def dead_menu_loop(self):
        clock = pygame.time.Clock()
        while self.dead_menu_show:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.game_ends()

                elif e.type == pygame.QUIT:
                    self.game_ends()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.button_restart_game.rect.collidepoint(pos):
                            self.start_game()
                        elif self.button_exit2.rect.collidepoint(pos):
                            self.game_ends()

            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.grave, (185, 120))
            self.text_money_result.draw(self.screen)
            self.button_restart_game.draw(self.screen)
            self.button_exit2.draw(self.screen)
            pygame.display.flip()
