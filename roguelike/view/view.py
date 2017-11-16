import pygame

from roguelike.enemy.meleeenemy import EasyMeleeEnemy
from roguelike.model.player import Player
from roguelike.model.world import World

room_color = (255, 255, 255)
wall_color = (255, 0, 0)
player_color = (0, 0, 255)
enemy_color = (0, 255, 0)


class View:
    def __init__(self, world: World):
        self.world: World = world

        surface_width = 8 * world.width
        surface_height = 8 * world.height
        self.main_surface = pygame.display.set_mode((surface_width, surface_height))

    def draw(self):
        self.main_surface.fill((0, 0, 0))

        for i in range(self.world.width):
            for j in range(self.world.height):
                tile = (i * 8, j * 8, 8, 8)
                # draw background
                if self.world.tiles[i][j].type == "R":
                    self.main_surface.fill(room_color, tile)
                elif self.world.tiles[i][j].type == "W":
                    self.main_surface.fill(wall_color, tile)
                elif self.world.tiles[i][j].type == "C":
                    self.main_surface.fill(room_color, tile)
                # draw characters
                if self.world.tiles[i][j].occupying_class == Player:
                    self.main_surface.fill(player_color, tile)
                if self.world.tiles[i][j].occupying_class == EasyMeleeEnemy:
                    self.main_surface.fill(enemy_color, tile)

        pygame.display.update()
