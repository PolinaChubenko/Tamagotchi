from set_interval import *
import random
from buttons import *
from unit import *


def event_loop(screen):
    while running:
        clock.tick(FPS)

        if pet.satiety <= 0 or pet.health <= 0:
            print("LOSE")
            game_ends()
        if pet.satiety >= 100 and pet.health >= 100:
            print("WIN")
            game_ends()

        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                if e.MyOwnType == ON_SATIETY:
                    pet.satiety -= random.randint(5, 20)
                    check_bottom()
                    update_text()

                elif e.MyOwnType == ON_HEALTH:
                    pet.health -= random.randint(5, 20)
                    check_bottom()
                    update_text()

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game_ends()

            elif e.type == pygame.QUIT:
                game_ends()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pos = pygame.mouse.get_pos()
                    if button_feed.rect.collidepoint(pos):
                        pet.satiety += 10
                        check_top()
                        update_text()
                        button_feed.call_back()

                    elif button_train.rect.collidepoint(pos):
                        pet.satiety -= 10
                        if pet.health >= 50:
                            pet.health += 10
                        else:
                            pet.health -= 15
                        check_bottom()
                        check_top()
                        update_text()
                        button_train.call_back()

                    if button_heal.rect.collidepoint(pos):
                        pet.satiety -= 10
                        if pet.health < 50:
                            pet.health += 15
                        else:
                            pet.health -= 20
                        check_bottom()
                        check_top()
                        update_text()
                        button_feed.call_back()

        update_state()
        draw_everything(screen)
        pygame.display.flip()


def update_text():
    text_satiety.change_text("satiety: {}".format(pet.satiety))
    text_health.change_text("health: {}".format(pet.health))


def check_bottom():
    if pet.satiety < 0:
        pet.satiety = 0
    if pet.health < 0:
        pet.health = 0


def check_top():
    if pet.satiety > 100:
        pet.satiety = 100
    if pet.health > 100:
        pet.health = 100


def update_state():
    if pet.satiety < 50:
        pet.update("hungry")
    if pet.satiety >= 50:
        if pet.health < 50:
            pet.update("unhealthy")
        else:
            pet.update("good")
    if pet.satiety <= 0:
        pet.update("died")


def draw_everything(screen):
    screen.fill(BACKGROUND_COLOR)
    for b in button_list:
        b.draw(screen)
    for t in text_list:
        t.draw(screen)
    screen.blit(pet.image, pet.rect)


def game_ends():
    global running
    running = False
    for it in interval_list:
        it.stop()


def game_init():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Tamagotchi")
    return pygame.display.set_mode(DISPLAY)


if __name__ == '__main__':
    game_screen = game_init()

    button_feed = Button((100, 100), BTN_SIZE, GRAY, PURPLE, text='Feed', font_size=FONT_SIZE)
    button_train = Button((240, 100), BTN_SIZE, GRAY, PURPLE, text='Train', font_size=FONT_SIZE)
    button_heal = Button((380, 100), BTN_SIZE, GRAY, PURPLE, text='Heal', font_size=FONT_SIZE)
    button_list = [button_feed, button_train, button_heal]

    states = "bad"
    pet = Pet()

    # text_i_am = Text("I am {}".format(pet.state), (210, 350), (0, 0, 0))
    text_satiety = Text("satiety: {}".format(pet.satiety), (55, 400), (255, 0, 0))
    text_health = Text("health: {}".format(pet.health), (200, 400), (255, 0, 0))
    text_list = [text_satiety, text_health]

    clock = pygame.time.Clock()

    satiety_event = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_SATIETY)
    feeding_event = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_HEALTH)

    interval_satiety = set_timer(satiety_event, 2)
    interval_feeding = set_timer(feeding_event, 2)
    interval_list = [interval_satiety, interval_feeding]

    running = True
    event_loop(game_screen)
    pygame.quit()
