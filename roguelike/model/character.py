from roguelike.model.entity import Entity
from roguelike.model.world.tile import Tile
from roguelike.model.world.world import World
from enum import Enum
from collections import namedtuple

Direction = namedtuple('Direction', ['x', 'y'])


class MovingDirections(Enum):
    DOWN = Direction(0, 1)
    UP = Direction(0, -1)
    LEFT = Direction(-1, 0)
    RIGHT = Direction(1, 0)

class Character(Entity):
    """
    Base class for all the stuff considered as alive (player, enemy etc)
    """

    def __init__(self, world: World):
        self.world = world
        self.hp: int = 100
        self.base_defense: int = 10
        self.base_attack: int = 10
        self.looking_direction = MovingDirections.UP
        self.occupied_tile = None

    def get_defense(self) -> int:
        return self.base_defense

    def on_damage(self, damage: int):
        self.hp = int(max(0, self.hp - (damage / self.get_defense())))

    def move(self, x, y):
        raise NotImplemented()

    def get_adjacent_reachable_tiles(self):
        reachable_tiles = []
        for dir in MovingDirections:
            new_x = self.occupied_tile.x + dir.value.x
            new_y = self.occupied_tile.y + dir.value.y
            if any((new_x, new_y)) < 0 or new_x > self.world.width or new_y > self.world.height:
                continue
            else:
                if self.world.tiles[new_x][new_y].passable:
                    reachable_tiles.append((new_x, new_y))
        return reachable_tiles