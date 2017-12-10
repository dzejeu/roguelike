import pygame

from roguelike.enemy.meleeenemy import DumbMeleeEnemy, BoundedEnemy
from roguelike.model.camera import Camera
from roguelike.model.player import Player
from roguelike.model.world import World
from roguelike.view.hud import Hud
from .assets import Assets
import sys;

sys.path.insert(0, "..")
from pgu import gui
from roguelike.model.character import MovingDirections

room_color = (255, 255, 255)
wall_color = (255, 0, 0)
player_color = (0, 0, 255)
enemy_color = (0, 255, 0)

tile_size = Assets.BASE_ASSET_SIZE


class View:
    def __init__(self, world: World, screen_width: int, screen_height: int, player):
        self.world: World = world

        self.screen_width = screen_width
        self.screen_height = screen_height

        surface_width = tile_size * world.width
        surface_height = tile_size * world.height

        self.main_surface = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.camera = Camera(surface_width, surface_height, screen_width, screen_height, tile_size)
        self.hud = Hud(self.main_surface, player)
        self.menu = None

    def draw(self, player):
        player_position = (player.occupied_tile.x, player.occupied_tile.y)
        self.main_surface.fill((0, 0, 0))
        self.camera.update(player_position)

        x_offset, y_offset = self.camera.apply()

        start_i = -self.camera.state.left // tile_size
        start_j = -self.camera.state.top // tile_size
        end_i = min(self.world.width, start_i + self.screen_width // tile_size + 1)
        end_j = min(self.world.height, start_j + self.screen_height // tile_size + 2)

        for i in range(start_i, end_i):
            for j in range(start_j, end_j):
                tile_asset = None

                # draw background
                if self.world.tiles[i][j].type == "R":
                    tile_asset = Assets.ROOM
                elif self.world.tiles[i][j].type == "W":
                    tile_asset = Assets.WALL
                elif self.world.tiles[i][j].type == "C":
                    tile_asset = Assets.CORRIDOR

                if tile_asset is not None:
                    tile = ((i * tile_size) + x_offset, (j * tile_size) + y_offset)
                    tile_asset.draw(self.main_surface, tile)

                    # there should not be any characters in void
                    # draw characters
                    if self.world.tiles[i][j].gold_dropped is not None:
                        Assets.GOLD.draw(self.main_surface, tile)
                    if self.world.tiles[i][j].occupied_by is not None:
                        if self.world.tiles[i][j].occupied_by.__class__ == DumbMeleeEnemy:
                            Assets.DUMB_ENEMY.draw(self.main_surface, tile)
                            self.hud.draw_character(self.world.tiles[i][j].occupied_by, tile)
                        if self.world.tiles[i][j].occupied_by.__class__ == Player:
                            if player.looking_direction == MovingDirections.UP:
                                Assets.PLAYER_BACK.draw(self.main_surface, tile)
                            elif player.looking_direction == MovingDirections.DOWN:
                                Assets.PLAYER_FRONT.draw(self.main_surface, tile)
                            elif player.looking_direction == MovingDirections.LEFT:
                                Assets.PLAYER_LEFT.draw(self.main_surface, tile)
                            elif player.looking_direction == MovingDirections.RIGHT:
                                Assets.PLAYER_RIGHT.draw(self.main_surface, tile)
                        if self.world.tiles[i][j].occupied_by.__class__ == BoundedEnemy:
                            Assets.BOUNDED_ENEMY.draw(self.main_surface, tile)
                            self.hud.draw_character(self.world.tiles[i][j].occupied_by, tile)
                    if self.world.tiles[i][j].mark_as_attacked > 0:
                        Assets.ATTACK.draw(self.main_surface, tile)
                        self.world.tiles[i][j].mark_as_attacked = max(
                            (self.world.tiles[i][j].mark_as_attacked - 1, 0))
                    if self.world.tiles[i][j].mark_as_attacked_by_enemy > 0:
                        Assets.ENEMY_ATTACK.draw(self.main_surface, tile)
                        self.world.tiles[i][j].mark_as_attacked_by_enemy = max(
                            (self.world.tiles[i][j].mark_as_attacked_by_enemy - 1, 0))

        self.hud.draw()
        if self.menu is not None:
            self.menu.draw()
            self.hud.draw_player_data()
        pygame.display.update()

    def draw_win_text(self):
        font = pygame.font.SysFont('monospace', 48)
        text = font.render("You've won!", False, (0, 255, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.main_surface.blit(text, text_rect)

    def draw_text(self, t):
        font = pygame.font.SysFont('monospace', 24)
        text = font.render(t, False, (0, 0, 255))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.main_surface.blit(text, text_rect)


