from math import pow, sqrt

from roguelike.enemy import BaseEnemy
from roguelike.model.world.tile import Tile
from roguelike.model.world.world import World
from roguelike.utils.pathfinding import get_adjacent_reachable_tiles, A_star_pathfinding, PathNotFound


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

    def chase_player(self, player_tile):
        best_tile = self.find_best_tile_to_move(player_tile)
        self.move(best_tile.x, best_tile.y)


class BoundedEnemy(BaseEnemy):
    def __init__(self, world: World):
        self._spawning_tile = None
        super().__init__(world)

    def get_distance(self, start: Tile, target: Tile):
        return sqrt(pow(float(start.x - target.x), 2) + pow(float(start.y - target.y), 2))

    def find_best_tile_to_move(self, target_tile):
        try:
            path_to_target = A_star_pathfinding(self.occupied_tile, target_tile, self.world)
            return path_to_target[-2]
        except PathNotFound:
            return self.occupied_tile

    @property
    def spawning_tile(self):
        if self._spawning_tile is None:
            self._spawning_tile = self.occupied_tile
        return self._spawning_tile

    def chase_player(self, player_tile):
        if self.get_distance(self.spawning_tile, self.occupied_tile) > (self.world.width / 10):
            tile_to_move = self.find_best_tile_to_move(self.spawning_tile)
        else:
            tile_to_move = self.find_best_tile_to_move(player_tile)
        self.move(tile_to_move.x, tile_to_move.y)

