import pygame
from pygame import *
from global_vars import *


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
        self.image.set_colorkey(WHITE, RLEACCEL)
