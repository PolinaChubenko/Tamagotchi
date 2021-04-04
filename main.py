from pygame import *
from set_interval import setInterval
import random
from buttons import *

WIN_WIDTH = 500
WIN_HEIGHT = 500
FPS = 60
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = WHITE

ON_SATIETY = 1
ON_HEALTH = 2


def set_timer(event_obj, interval):
    return setInterval(func=lambda x: pygame.event.post(x), sec=interval, args=[event_obj])


class Pet(pygame.sprite.Sprite):
    def __init__(self, state="good"):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self.satiety = 80
        self.health = 80
        self.image_path = "imgs/{}.png".format(self.state)
        self.image = pygame.image.load(self.image_path).convert()
        self.image.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH / 2, WIN_WIDTH / 2)

    def update(self, new_state):
        self.state = new_state
        self.image_path = "imgs/{}.png".format(self.state)
        self.image = pygame.image.load(self.image_path).convert()


def fn1():
    print('button1')


def fn2():
    print('button2')


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tamagotchi")

    size = 10
    clr = [255, 0, 255]
    bg = (255, 255, 0)
    font_size = 25
    font = pygame.font.Font(None, font_size)

    button_feed = Button(position=(100, 100), size=(100, 50), clr=(220, 220, 220), cngclr=GREEN,
                         func=fn1, text='Feed', font_size=font_size)
    button_train = Button((240, 100), (100, 50), (220, 220, 220), GREEN, fn2, 'Train', font_size=font_size)

    button_list = [button_feed, button_train]

    clock = pygame.time.Clock()

    states = "bad"
    pet = Pet()

    # button = pygame.Rect(100, 100, 50, 50)

    # pygame.time.set_timer(pygame.USEREVENT, 2000)
    SatietyEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_SATIETY)
    FeedingEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_HEALTH)
    Interval_Satiety = set_timer(SatietyEvent, 2)
    Interval_Feeding = set_timer(FeedingEvent, 2)
    running = True
    is_victory = -1
    while running:
        clock.tick(FPS)

        if pet.satiety <= 0:
            running = False
            is_victory = False
            Interval_Satiety.stop()
            Interval_Feeding.stop()
        if pet.satiety >= 100:
            running = False
            is_victory = True
            Interval_Satiety.stop()
            Interval_Feeding.stop()

        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:
                if event.MyOwnType == ON_HEALTH:
                    pet.health -= random.randint(5, 20)
                    if pet.health < 0:
                        pet.health = 0
                    # print("Health change:", pet.health)
                if event.MyOwnType == ON_SATIETY:
                    pet.satiety -= random.randint(5, 20)
                    if pet.satiety < 0:
                        pet.satiety = 0
                    # print("Satiety change:", pet.satiety)

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    Interval_Satiety.stop()
                    Interval_Feeding.stop()

            elif event.type == pygame.QUIT:
                running = False
                Interval_Satiety.stop()
                Interval_Feeding.stop()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if button_feed.rect.collidepoint(pos):
                        pet.satiety += 10
                        print("You have fed you pet", pet.satiety)
                        button_feed.call_back()
                    elif button_train.rect.collidepoint(pos):
                        pet.satiety -= 10
                        if pet.health >= 50:
                            pet.health += 10
                        else:
                            pet.health -= 15
                        print("You have trained you pet", pet.health)
                        button_train.call_back()

        screen.fill(BACKGROUND_COLOR)

        for b in button_list:
            b.draw(screen)

        if pet.satiety < 50:
            pet.update("hungry")
        if pet.satiety >= 50:
            pet.update("good")
        if pet.satiety <= 0:
            pet.update("died")

        screen.blit(pet.image, pet.rect)
        # pygame.draw.rect(screen, [255, 0, 0], button)  # draw button
        pygame.display.flip()

    if is_victory != -1:
        if is_victory:
            print("WIN")
        else:
            print("LOSE")
        pygame.time.wait(5000)

    pygame.quit()
