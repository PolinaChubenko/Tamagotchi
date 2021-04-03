import pygame
from pygame import *
from set_interval import setInterval

WIN_WIDTH = 500
WIN_HEIGHT = 500
FPS = 60
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = WHITE

ON_SATIETY_LOWERS = 1
ON_MOOD_CHANGE = 2


def set_timer(event_obj, interval):
    return setInterval(func=lambda x: pygame.event.post(x), sec=interval, args=[event_obj])


class Pet(pygame.sprite.Sprite):
    def __init__(self, state="good"):
        pygame.sprite.Sprite.__init__(self)
        self.satiety = 80
        self.image_path = "imgs/{}.png".format(state)
        self.image = pygame.image.load(self.image_path).convert()
        self.image.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH / 2, WIN_WIDTH / 2)

    def update(self, new_state):
        self.image_path = "imgs/{}.png".format(new_state)
        self.image = pygame.image.load(self.image_path).convert()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tamagotchi")
    clock = pygame.time.Clock()

    states = "bad"
    player = Pet(states)

    # pygame.time.set_timer(pygame.USEREVENT, 2000)
    SatietyEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_SATIETY_LOWERS)
    MoodEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_MOOD_CHANGE)
    myIntervalHandle1 = set_timer(SatietyEvent, 2)
    myIntervalHandle2 = set_timer(MoodEvent, 2)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.MyOwnType == ON_MOOD_CHANGE:
                    print("Mood change")
                    if states == "bad":
                        states = "good"
                    else:
                        states = "bad"
                elif event.MyOwnType == ON_SATIETY_LOWERS:
                    player.satiety -= 5
                    print("Satiety change:", player.satiety)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    myIntervalHandle1.stop()
                    myIntervalHandle2.stop()
            elif event.type == pygame.QUIT:
                running = False
                myIntervalHandle1.stop()
                myIntervalHandle2.stop()

        screen.fill(BACKGROUND_COLOR)
        player.update(states)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

    pygame.quit()
