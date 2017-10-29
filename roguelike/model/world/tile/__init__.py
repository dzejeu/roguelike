from enum import Enum, auto

from .basetile import BaseTile
from .ground import Ground


class Tile(Enum):
    GROUND = (Ground, 1)

    def __new__(cls, tile_type, value=None, *args, **kwargs):
        if value is None:
            value = auto()
        obj = object.__new__(cls)
        obj._value_ = value
        obj._tile_type_ = tile_type
        return obj

    def __call__(self, *args, **kwargs) -> BaseTile:
        return self._tile_type_(*args, **kwargs)
