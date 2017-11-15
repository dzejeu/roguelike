from roguelike.model.character import Character, Direction
from roguelike.model.world.world import World


class Player(Character):
    def __init__(self, world: World):
        super().__init__(world)
        self.position = Direction(None, None)

    def move(self, x, y):
        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.occupied_tile is not None:
                self.occupied_tile.leave()
            self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)
            self.position = Direction(x, y)
