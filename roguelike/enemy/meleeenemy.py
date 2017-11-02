from roguelike.enemy import BaseEnemy
from roguelike.model.world.tile import Tile
from roguelike.model.character import MovingDirections
import random


class EasyMeleeEnemy(BaseEnemy):
    def find_best_direction_to_move(self, target_tile):
        direction_to_move = (target_tile.x - self.occupied_tile.x, target_tile.y - self.occupied_tile.y)
        direction_to_move = (direction_to_move[0] if direction_to_move[0] == 0 else direction_to_move[0] / abs(direction_to_move[0]),
                             direction_to_move[1] if direction_to_move[1] == 0 else direction_to_move[1] / abs(direction_to_move[1]))
        return MovingDirections(direction_to_move)

    def move(self, x, y):
        if self.occupied_tile is not None:
            self.occupied_tile.leave()
        self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)

    def chase_player(self, player_tile):
        target_direction = self.find_best_direction_to_move(player_tile)
        available_moves = set(MovingDirections)
        while available_moves:
            best_move = min(available_moves, key=lambda var:
            abs(target_direction.value.x - var.value.x) + abs(target_direction.value.y - var.value.y))
            if self.world.tiles[self.occupied_tile.x + best_move.value.x][self.occupied_tile.y + best_move.value.y].passable:
                self.move(self.occupied_tile.x + best_move.value.x, self.occupied_tile.y + best_move.value.y)
                break
            else:
                available_moves.remove(best_move)
