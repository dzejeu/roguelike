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

    @staticmethod
    def get_direction_from_diff(old, new):
        dx = new[0] - old[0]
        dy = new[1] - old[1]

        if abs(dx) > abs(dy):
            if dx > 0:
                return MovingDirections.RIGHT
            else:
                return MovingDirections.LEFT
        else:
            if dy > 0:
                return MovingDirections.DOWN
            else:
                return MovingDirections.UP


class Character(Entity):
    """
    Base class for all the stuff considered as alive (player, enemy etc)
    """

    def __init__(self, world: World):
        self.world = world
        self.hp: int = 100
        self.max_hp: int = 100
        self.base_defense: int = 10
        self.base_attack: int = 10
        self.looking_direction = MovingDirections.UP
        self.occupied_tile = None

    def check_if_alived(self):
        pass

    def get_defense(self) -> int:
        return self.base_defense

    def on_damage(self, damage: int):
        self.hp = int(max(0, self.hp - (damage / self.get_defense())))

    def move(self, x, y):
        raise NotImplemented()