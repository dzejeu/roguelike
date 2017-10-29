from typing import List

from .chunk import Chunk
from model.entity import Entity


class World:
    def __init__(self):
        self.chunks: List[Chunk] = []
        self.entities: List[Entity] = []
