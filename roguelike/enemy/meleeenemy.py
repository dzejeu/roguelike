from roguelike.enemy import BaseEnemy
from roguelike.model.world.tile import Tile
from roguelike.model.character import MovingDirections
import random
from math import pow, sqrt


class EasyMeleeEnemy(BaseEnemy):
    def _get_euclidean_distance(self, x, y, x_target, y_target):
        return sqrt(pow(float(x - x_target), 2) + pow(float(y - y_target), 2))

    def find_best_tile_to_move(self, target_tile):
        reachable_tiles = self.get_adjacent_reachable_tiles()
        return min(reachable_tiles,
                   key=lambda tile: self._get_euclidean_distance(tile[0], tile[1], target_tile.x, target_tile.y))

    def move(self, x, y):
        if self.occupied_tile is not None:
            self.occupied_tile.leave()
        self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)

    def chase_player(self, player_tile):
        tile_to_move = self.find_best_tile_to_move(player_tile)
        self.move(tile_to_move[0], tile_to_move[1])