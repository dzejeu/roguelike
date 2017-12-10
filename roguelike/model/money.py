

class Gold(object):
    def __init__(self, tile_to_drop, amount):
        self.tile_to_drop = tile_to_drop
        self.amount = amount

    def drop(self):
        self.tile_to_drop.gold_dropped = self