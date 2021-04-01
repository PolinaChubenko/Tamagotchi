import pygame
from pygame import *

WIN_WIDTH = 500
WIN_HEIGHT = 500
FPS = 60
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = WHITE


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

    pygame.time.set_timer(pygame.USEREVENT, 2000)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if states == "bad":
                    states = "good"
                else:
                    states = "bad"
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        player.update(states)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

    pygame.quit()
