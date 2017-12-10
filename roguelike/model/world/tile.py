class Tile:
    breakable = False
    collidable = False
    passable = True
    occupied_by = None
    type = "V" #types of tiles V - void, R - room, C - corridor, W - wall, O - obstacle, easily expandable
    mark_as_attacked = 0
    mark_as_attacked_by_enemy = 0
    gold_dropped = None     # jezeli gold lezy na tile'u to pod to pole bd podpiety obiekt golda

    def __init__(self):
        self.occupied_by = None

    @classmethod
    def on_position(cls, x, y, default_type='V'):
        tile = cls()
        tile.set_position(x, y)
        tile.type = default_type
        return tile

    def occupy(self, occupied_by):
        """
        :param occupied_by: this provides info about who/what is standing on a tile
        :return:
        """
        self.passable = False
        self.collidable = True
        self.occupied_by = occupied_by
        return self

    def leave(self):
        self.passable = True
        self.collidable = False
        self.occupied_by = None

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def get_position(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + str(self.y))