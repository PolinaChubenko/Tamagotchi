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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/good.png").convert()
        self.image.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH / 2, WIN_WIDTH / 2)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tamagotchi")
    clock = pygame.time.Clock()

    player = Pet()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        pygame.display.flip()

    pygame.quit()
