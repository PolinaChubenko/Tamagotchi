import pygame


class Button:
    def __init__(self, position, size, color=None, hover_color=None,
                 func=None, text='', font="Segoe Print", font_size=16, font_clr=None):
        if color is None:
            color = [100, 100, 100]
        if font_clr is None:
            font_clr = [0, 0, 0]
        self.color = color
        self.current_color = self.color
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if hover_color:
            self.hover_color = hover_color
        else:
            self.hover_color = color

        if len(color) == 4:
            self.surf.set_alpha(color[3])

        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_color = font_clr
        self.txt_surface = self.font.render(self.txt, True, self.font_color)
        self.txt_rect = self.txt_surface.get_rect(center=[wh // 2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.current_color)
        self.surf.blit(self.txt_surface, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.current_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color

    def call_back(self, *args):
        if self.func:
            return self.func(*args)


class Text:
    def __init__(self, msg, position, clr=None, font="Segoe Print", font_size=25, mid=False):
        if clr is None:
            clr = [100, 100, 100]
        self.clr = clr
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, True, self.clr)

        if len(self.clr) == 4:
            self.txt_surf.set_alpha(self.clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)

    def change_text(self, new_msg):
        self.txt_surf = self.font.render(new_msg, True, self.clr)

    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)
