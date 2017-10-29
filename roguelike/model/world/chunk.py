from typing import List

from .tile import Tile


class Chunk:
    def __init__(self, size: int = 64):
        self.top: Chunk = None
        self.right: Chunk = None
        self.bottom: Chunk = None
        self.left: Chunk = None
        self.data: List[List[Tile]] = [[None for _ in range(size)] for _ in range(size)]
