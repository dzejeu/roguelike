import random
from math import pow, sqrt
from collections import deque

import numpy

from roguelike.enemy import BaseEnemy
from roguelike.model import player
from roguelike.model.money import Gold
from roguelike.model.world.tile import Tile
from roguelike.model.world.world import World
from roguelike.utils.pathfinding import get_adjacent_reachable_tiles, A_star_pathfinding, PathNotFound, \
    get_manhattan_distance, get_euclidean_distance


class Ghost(BaseEnemy):
    def __init__(self, world: World):
        super().__init__(world)
        self.base_attack = 130

    def find_best_tile_to_move(self, target_tile):
        reachable_tiles = get_adjacent_reachable_tiles(self.occupied_tile, self.world)
        if reachable_tiles:
            return min(reachable_tiles,
                       key=lambda tile: get_euclidean_distance(tile, target_tile))
        else:
            return self.occupied_tile

    def check_if_alived(self):
        if self.hp == 0:
            self.occupied_tile.leave()
            gold = Gold(self.occupied_tile, random.randint(1, 6))
            gold.drop()
            return False
        return True

    def chase_player(self, player_tile):
        if get_manhattan_distance(self.occupied_tile, player_tile) < 35:
            best_tile = self.find_best_tile_to_move(player_tile)
            self.move(best_tile.x, best_tile.y)
        else:
            [tile_to_move] = random.sample(get_adjacent_reachable_tiles(self.occupied_tile, self.world), 1)
            self.move(tile_to_move.x, tile_to_move.y)
        self.attack()


class Skeleton(BaseEnemy):
    def __init__(self, world: World):
        self.counter = 0
        self.memory = deque()
        self._spawning_tile = None
        super().__init__(world)
        self.base_attack = 90
        self.base_defense = 100

    def reduce_world(self, reduction):
        if self.occupied_tile.x - reduction >= 0:
            left_bound = self.occupied_tile.x - reduction
        else:
            left_bound = 0
        if self.occupied_tile.x + reduction < self.world.width:
            right_bound = self.occupied_tile.x + reduction
        else:
            right_bound = self.world.width - 1
        if self.occupied_tile.y - reduction >= 0:
            lower_bound = self.occupied_tile.y - reduction
        else:
            lower_bound = 0
        if self.occupied_tile.y + reduction < self.world.height:
            upper_bound = self.occupied_tile.y + reduction
        else:
            upper_bound = self.world.height - 1
        all_tiles = numpy.array(self.world.tiles)
        tiles = all_tiles[left_bound:right_bound, lower_bound:upper_bound]
        reduced_world = World(right_bound - left_bound, upper_bound - lower_bound)
        reduced_world.tiles = tiles
        return reduced_world

    def find_best_tile_to_move(self, target_tile):
        try:
            path = A_star_pathfinding(self.occupied_tile, target_tile, self.reduce_world(30))
        except (IndexError, PathNotFound):
            return []
        return path[:-1]

    def support_pathfinding(self, target_tile):
        reachable_tiles = get_adjacent_reachable_tiles(self.occupied_tile, self.world)
        if reachable_tiles:
            return min(reachable_tiles,
                       key=lambda tile: get_manhattan_distance(tile, target_tile))
        else:
            return self.occupied_tile

    @property
    def spawning_tile(self):
        if self._spawning_tile is None:
            self._spawning_tile = self.occupied_tile
        return self._spawning_tile

    def check_if_alived(self):
        if self.hp == 0:
            self.occupied_tile.leave()
            gold = Gold(self.occupied_tile, random.randint(4, 12))
            gold.drop()
            return False
        return True

    def chase_player(self, player_tile):
        if self.counter != 0:
            if get_manhattan_distance(self.occupied_tile, player_tile) < 20:
                try:
                    tile_to_move = self.memory.pop()
                except (PathNotFound, IndexError):
                    tile_to_move = self.support_pathfinding(player_tile)
            else:
                [tile_to_move] = random.sample(get_adjacent_reachable_tiles(self.occupied_tile, self.world), 1)
        else:
            if get_manhattan_distance(self.occupied_tile, player_tile) < 20:
                self.memory = deque(self.find_best_tile_to_move(player_tile))
                if self.memory:
                    tile_to_move = self.memory.pop()
                else:
                    tile_to_move = self.support_pathfinding(player_tile)
            else:
                tile_to_move = self.support_pathfinding(player_tile)
        self.counter = (self.counter + 1) % 25
        self.move(tile_to_move.x, tile_to_move.y)
        self.attack()

class Demon(Skeleton):
    def __init__(self, world: World):
        super().__init__(world)
        self.base_attack = 350
        self.base_defense = 120
        self.slow_factor = 0

    def check_if_alived(self):
        if self.hp == 0:
            self.occupied_tile.leave()
            gold = Gold(self.occupied_tile, random.randint(26, 45))
            gold.drop()
            return False
        return True

    def chase_player(self, player_tile):
        if self.slow_factor == 0:
            if self.counter != 0:
                if get_manhattan_distance(self.occupied_tile, player_tile) < 20:
                    try:
                        tile_to_move = self.memory.pop()
                    except (PathNotFound, IndexError):
                        tile_to_move = self.support_pathfinding(player_tile)
                else:
                    tile_to_move = self.support_pathfinding(player_tile)
            else:
                if get_manhattan_distance(self.occupied_tile, player_tile) < 20:
                    if self.memory:
                        tile_to_move = self.memory.pop()
                    else:
                        self.memory = deque(self.find_best_tile_to_move(player_tile))
                        if self.memory:
                            tile_to_move = self.memory.pop()
                        else:
                            tile_to_move = self.support_pathfinding(player_tile)
                else:
                    tile_to_move = self.support_pathfinding(player_tile)
            self.counter = (self.counter + 1) % 20
            self.move(tile_to_move.x, tile_to_move.y)
        self.slow_factor = (self.slow_factor + 1) % 2
        self.attack()

class CrazyFrog(BaseEnemy):
    def __init__(self, world: World):
        super().__init__(world)
        self.base_attack = 400
        self.base_defense = 1

    def attack(self):
        neighbours = get_adjacent_reachable_tiles(self.occupied_tile, self.world)
        for neighbour in neighbours:
            if neighbour.occupied_by.__class__ == player.Player:
                neighbour.occupied_by.on_damage(self.base_attack)
                for neighbour in neighbours:
                    neighbour.mark_as_poisoned = 6
                self.hp = 0
                break

    def check_if_alived(self):
        if self.hp == 0:
            self.occupied_tile.leave()
            gold = Gold(self.occupied_tile, random.randint(1, 3))
            gold.drop()
            return False
        return True

    def chase_player(self, player_tile):
        [tile_to_move] = random.sample(get_adjacent_reachable_tiles(self.occupied_tile, self.world), 1)
        self.move(tile_to_move.x, tile_to_move.y)
        self.attack()