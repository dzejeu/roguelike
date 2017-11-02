from collections import namedtuple

Rect = namedtuple('Rect', ['top', 'right', 'bottom', 'left'])


class Tile:
    breakable = False
    collidable = False
    passable = True
    occupying_class = None

    def __init__(self, size: int = 20):
        self.rect = Rect(*(None for _ in range(4)))
        self.size = size

    @classmethod
    def on_position(cls, x, y):
        chunk = cls()
        chunk.set_rect(Rect(y * chunk.size, x * chunk.size + chunk.size,
                            y * chunk.size + chunk.size, x * chunk.size))
        chunk.set_position(x, y)
        return chunk

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
        self.set_rect(Rect(new_y * self.size, new_x * self.size + self.size,
                            new_y * self.size + self.size, new_x * self.size))

    def get_position(self):
        return self.x, self.y

    def set_rect(self, rect: Rect):
        self.rect = rect

    def __eq__(self, other):
        return self.rect.__eq__(other.rect)

    def __hash__(self):
        return self.rect.__hash__()
