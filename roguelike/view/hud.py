import pygame

from roguelike.view.assets import Assets


class Hud:
    MAIN_BAR_HEIGHT = 8
    MAIN_BAR_WIDTH = 100
    BAR_HEIGHT = 3
    BAR_PADDING = 1
    BAR_WIDTH = Assets.BASE_ASSET_SIZE - BAR_PADDING*2
    MARGIN = 10
    BAR_MARGIN = -6
    HP_COLOR = (255, 0, 0)
    HP_BG_COLOR = (20, 0, 0)

    def __init__(self, surface, player):
        self.player = player
        self.surface: pygame.Surface = surface
        self.player_hp_bg_position = (Hud.MARGIN, Hud.MARGIN, Hud.MAIN_BAR_WIDTH, Hud.MAIN_BAR_HEIGHT)
        self.character_queue = []

    def draw(self):
        for character in self.character_queue:
            position = (Hud.BAR_PADDING + character[1][0], character[1][1] + Hud.BAR_MARGIN, Hud.BAR_WIDTH, Hud.BAR_HEIGHT)
            self.draw_character_data(character[0], position)
        self.character_queue.clear()
        self.draw_player_data()

    def draw_character(self, character, position):
        self.character_queue.append((character, position))

    def draw_player_data(self):
        self.draw_character_data(self.player, self.player_hp_bg_position)

    def draw_character_data(self, character, position):
        self.surface.fill(Hud.HP_BG_COLOR, position)
        hp_percentage = character.hp / character.max_hp
        hp_position = (position[0], position[1],
                       position[2] * hp_percentage, position[3] * hp_percentage)
        self.surface.fill(Hud.HP_COLOR, hp_position)
