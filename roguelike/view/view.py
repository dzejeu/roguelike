import pygame

from roguelike.enemy.meleeenemy import EasyMeleeEnemy
from roguelike.model.player import Player
from roguelike.model.world import World
from roguelike.model.camera import Camera

room_color = (255, 255, 255)
wall_color = (255, 0, 0)
player_color = (0, 0, 255)
enemy_color = (0, 255, 0)

tile_size = 8

class View:
    def __init__(self, world: World, screen_width:int, screen_height:int):
        self.world: World = world

        screen_width = screen_width
        screen_height = screen_height

        surface_width = tile_size * world.width
        surface_height = tile_size * world.height

        self.main_surface = pygame.display.set_mode((screen_width, screen_height))
        self.camera = Camera(surface_width, surface_height, screen_width, screen_height, tile_size)

    def draw(self, player_position):
        self.main_surface.fill((0, 0, 0))
        self.camera.update(player_position)

        x_offset, y_offset = self.camera.apply()

        for i in range(self.world.width):
            for j in range(self.world.height):
                tile = ((i * tile_size)+x_offset , (j * tile_size)+y_offset, tile_size, tile_size)
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
