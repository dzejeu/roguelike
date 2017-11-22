class Tile:
    breakable = False
    collidable = False
    passable = True
    occupying_class = None
    type = "V" #types of tiles V - void, R - room, C - corridor, W - wall, O - obstacle, easily expandable

    def __init__(self):
        self.occupying_class = None

    @classmethod
    def on_position(cls, x, y, default_type='V'):
        tile = cls()
        tile.set_position(x, y)
        tile.type = default_type
        return tile

    def occupy(self, occupying_class):
        """
        :param occupying_class: this provides info about who/what is standing on a tile
        :return:
        """
        self.passable = False
        self.collidable = True
        self.occupying_class = occupying_class
        return self

    def leave(self):
        self.passable = True
        self.collidable = False
        self.occupying_class = None

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def get_position(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + str(self.y))