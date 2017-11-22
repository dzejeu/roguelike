from math import pow, sqrt

from roguelike.enemy import BaseEnemy
from roguelike.utils.pathfinding import get_adjacent_reachable_tiles


class DumbMeleeEnemy(BaseEnemy):
    def _get_euclidean_distance(self, x, y, x_target, y_target):
        return sqrt(pow(float(x - x_target), 2) + pow(float(y - y_target), 2))

    def find_best_tile_to_move(self, target_tile):
        reachable_tiles = get_adjacent_reachable_tiles(self.occupied_tile, self.world)
        if reachable_tiles:
            return min(reachable_tiles,
                       key=lambda tile: self._get_euclidean_distance(tile.x, tile.y, target_tile.x, target_tile.y))
        else:
            return self.occupied_tile

    def move(self, x, y):
        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.world.tiles[x][y].passable:
                if self.occupied_tile is not None:
                    self.occupied_tile.leave()
                self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)

    def chase_player(self, player_tile):
        best_tile = self.find_best_tile_to_move(player_tile)
        self.move(best_tile.x, best_tile.y)

