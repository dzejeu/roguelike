from collections import namedtuple


class Tile:
    breakable = False
    collidable = False
    passable = True
    occupying_class = None

    def __init__(self):
        self.rect = Rect(*(None for _ in range(4)))

    @classmethod
    def on_position(cls, x, y):
        tile = cls()
        tile.set_position(x, y)
        return tile

    def occupy(self, occupying_class):
        self.passable = False
        self.collidable = True
        self.occupying_class = occupying_class
        return self

    def leave(self):
        self.passable = True
        self.collidable = False

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def get_position(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

