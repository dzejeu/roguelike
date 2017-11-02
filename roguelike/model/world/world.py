from typing import List

from roguelike.model.world.tile import Tile
from roguelike.model.entity import Entity


class World:
    def __init__(self, width, height):
        """
        :param width: amount of tiles in x axis
        :param height: amount of tiles in y axis
        """
        self.tiles: List[List[Tile]] = [[Tile.on_position(h, w) for w in range(width)] for h in range(height)]
        self.entities: List[Entity] = []
