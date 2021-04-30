import pygame
from classes.global_vars import *
from classes.state import PetState, Good
import random


class Pet(pygame.sprite.Sprite):
    _state = None

    def __init__(self, state: PetState = Good()):
        pygame.sprite.Sprite.__init__(self)
        self.transition_to(state)
        self.satiety = 80
        self.health = 80
        self.happiness = 80
        self.money = 0
        self.money_delta = 10
        self.image_path = "imgs/{}.png".format(str(type(state).__name__).lower())
        self.image = pygame.image.load(self.image_path).convert()
        self.image.set_colorkey(WHITE, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH / 2 - 70, WIN_HEIGHT / 2)

    def transition_to(self, state: PetState):
        self.update_img(str(type(state).__name__).lower())
        self._state = state
        self._state.pet = self

    def update_state(self):
        self._state.update_state()

    def update_img(self, new_state):
        self.image_path = "imgs/{}.png".format(new_state)
        self.image = pygame.image.load(self.image_path).convert()
        self.image.set_colorkey(WHITE, pygame.RLEACCEL)

    def refresh_params(self):
        self.satiety = 80
        self.health = 80
        self.happiness = 80
        self.money = 0
        self.money_delta = 10
        self.update("good")

    def life_cycle(self, lose=0, win=100):
        self.satiety -= random.randint(5, 20)
        self.health -= random.randint(5, 20)
        self.happiness -= random.randint(5, 20)
        self.check_params(lose, win)

    def check_params(self, lose=0, win=100):
        if self.satiety < lose:
            self.satiety = lose
        if self.health < lose:
            self.health = lose
        if self.satiety > win:
            self.satiety = win
        if self.health > win:
            self.health = win

    def feed(self):
        self.satiety += 10
        self.check_params()

    def train(self, mid=50):
        self.satiety -= 10
        if self.health >= mid:
            self.health += 10
        else:
            self.health -= 15
        self.check_params()

    def heal(self, mid=50):
        self.satiety -= 10
        self.happiness -= 5
        if self.health < mid:
            self.health += 15
        else:
            self.health -= 20
        self.check_params()

    def play(self):
        self.satiety -= 15
        self.happiness += 15
        self.check_params()

    def work(self):
        if self.happiness > 0:
            self.money += self.money_delta
            self.money_delta += 1
            self.satiety -= 10
            self.health -= 10
            self.happiness -= 10
            self.check_params()
