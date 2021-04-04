from set_interval import *
import random
from buttons import *
from unit import *


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tamagotchi")

    btn_size = (100, 50)
    font_size = 25
    button_feed = Button((100, 100), btn_size, GRAY, PURPLE, text='Feed', font_size=font_size)
    button_train = Button((240, 100), btn_size, GRAY, PURPLE, text='Train', font_size=font_size)
    button_list = [button_feed, button_train]

    states = "bad"
    pet = Pet()

    # text_i_am = Text("I am {}".format(pet.state), (210, 350), (0, 0, 0))
    text_satiety = Text("satiety: {}".format(pet.satiety), (55, 400), (255, 0, 0))
    text_health = Text("health: {}".format(pet.health), (200, 400), (255, 0, 0))
    text_list = [text_satiety, text_health]

    clock = pygame.time.Clock()

    SatietyEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_SATIETY)
    FeedingEvent = pygame.event.Event(pygame.USEREVENT, MyOwnType=ON_HEALTH)
    Interval_Satiety = set_timer(SatietyEvent, 2)
    Interval_Feeding = set_timer(FeedingEvent, 2)
    Interval_list = [Interval_Satiety, Interval_Feeding]

    running = True
    is_victory = -1

    def game_ends():
        global running, Interval_list
        running = False
        for it in Interval_list:
            it.stop()

    while running:
        clock.tick(FPS)

        if pet.satiety <= 0 or pet.health <= 0:
            is_victory = False
            print("LOSE")
            game_ends()
        if pet.satiety >= 100 or pet.health >= 100:
            is_victory = True
            print("WIN")
            game_ends()

        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:
                if event.MyOwnType == ON_SATIETY:
                    pet.satiety -= random.randint(5, 20)
                    if pet.satiety < 0:
                        pet.satiety = 0
                    text_satiety.change_text("satiety: {}".format(pet.satiety))
                elif event.MyOwnType == ON_HEALTH:
                    pet.health -= random.randint(5, 20)
                    if pet.health < 0:
                        pet.health = 0
                    text_health.change_text("health: {}".format(pet.health))
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_ends()

            elif event.type == pygame.QUIT:
                game_ends()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if button_feed.rect.collidepoint(pos):
                        pet.satiety += 10
                        text_satiety.change_text("satiety: {}".format(pet.satiety))
                        button_feed.call_back()
                    elif button_train.rect.collidepoint(pos):
                        pet.satiety -= 10
                        text_satiety.change_text("health: {}".format(pet.satiety))
                        if pet.health >= 50:
                            pet.health += 10
                        else:
                            pet.health -= 15
                        text_health.change_text("satiety: {}".format(pet.health))
                        button_train.call_back()

        screen.fill(BACKGROUND_COLOR)

        for b in button_list:
            b.draw(screen)

        for t in text_list:
            t.draw(screen)

        if pet.satiety < 50:
            pet.update("hungry")
        if pet.satiety >= 50:
            if pet.health < 50:
                pet.update("unhealthy")
            else:
                pet.update("good")
        if pet.satiety <= 0:
            pet.update("died")

        screen.blit(pet.image, pet.rect)
        pygame.display.flip()

    pygame.quit()
