from set_interval import *
from buttons import *
from unit import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Tamagotchi")
        self.game_screen = pygame.display.set_mode(DISPLAY)

        self.states = "bad"
        self.pet = Pet()

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

        self.interval_life_cycle = set_timer(self.life_cycle_event, 2)

        self.running = True

    def start_game(self):
        self.running = True
        self.event_loop()

    def game_ends(self):
        self.running = False
        self.interval_life_cycle.stop()

    def check_victory(self, lose=0, win=100):
        if self.pet.satiety <= lose or self.pet.health <= lose:
            print("LOSE")
            self.game_ends()
        elif self.pet.satiety >= win and self.pet.health >= win\
                and self.pet.happiness >= win:
            print("WIN")
            self.game_ends()

    def event_loop(self):
        clock = pygame.time.Clock()
        while self.running:
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
        self.game_screen.fill(BACKGROUND_COLOR)
        for b in self.button_list:
            b.draw(self.game_screen)
        for t in self.text_list:
            t.draw(self.game_screen)
        self.pet.draw(self.game_screen)
