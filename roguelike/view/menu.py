import pygame


class Menu:
    TEXT_COLOR = (255, 255, 255)
    GRAY_TEXT_COLOR = (200, 150, 150)
    BG_COLOR = (0, 0, 0)
    MARGIN = 10
    MARGIN_LEFT = 100

    def __init__(self, data, surface: pygame.Surface, player):
        self.data = data
        self.player = player
        self.surface: pygame.Surface = surface
        self.size = surface.get_size()
        self.bg = pygame.Surface(self.size)
        self.bg.set_alpha(230)
        self.bg.fill(Menu.BG_COLOR)

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        font = pygame.font.SysFont('monospace', 24)
        text = font.render(self.data.name, False, Menu.TEXT_COLOR)
        text_rect = text.get_rect(center=(self.size[0] / 2, 20))
        self.surface.blit(text, text_rect)

        i = 1
        position = text_rect.bottom + Menu.MARGIN * 2
        for option in self.data.options:
            color = Menu.TEXT_COLOR if self.data.available(i - 1) else Menu.GRAY_TEXT_COLOR
            item_text = font.render("{}) {}".format(i, option.info), False, color)
            item_text_rect = text.get_rect()
            item_text_rect[0] = Menu.MARGIN_LEFT
            item_text_rect[1] = position
            self.surface.blit(item_text, item_text_rect)
            position = item_text_rect.bottom + Menu.MARGIN
            i += 1


