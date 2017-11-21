import pygame

from roguelike.enemy.meleeenemy import EasyMeleeEnemy
from roguelike.model.camera import Camera
from roguelike.model.player import Player
from roguelike.model.world import World
from .assets import Assets

room_color = (255, 255, 255)
wall_color = (255, 0, 0)
player_color = (0, 0, 255)
enemy_color = (0, 255, 0)

tile_size = Assets.BASE_ASSET_SIZE

class View:
    def __init__(self, world: World, screen_width:int, screen_height:int):
        self.world: World = world

        self.screen_width = screen_width
        self.screen_height = screen_height

        surface_width = tile_size * world.width
        surface_height = tile_size * world.height

        self.main_surface = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)
        self.camera = Camera(surface_width, surface_height, screen_width, screen_height, tile_size)

    def draw(self, player_position):
        self.main_surface.fill((0, 0, 0))
        self.camera.update(player_position)

        x_offset, y_offset = self.camera.apply()

        for i in range(self.world.width):
            for j in range(self.world.height):
                tile = ((i * tile_size)+x_offset , (j * tile_size)+y_offset)
                tile_asset = None

                # draw background
                if self.world.tiles[i][j].type == "R":
                    tile_asset = Assets.ROOM
                elif self.world.tiles[i][j].type == "W":
                    tile_asset = Assets.WALL
                elif self.world.tiles[i][j].type == "C":
                    tile_asset = Assets.CORRIDOR

                if tile_asset is not None:
                    tile_asset.draw(self.main_surface, tile)

                # draw characters
                if self.world.tiles[i][j].occupying_class == EasyMeleeEnemy:
                    Assets.ENEMY.draw(self.main_surface, tile)
                if self.world.tiles[i][j].occupying_class == Player:
                    Assets.PLAYER.draw(self.main_surface, tile)

        pygame.display.update()