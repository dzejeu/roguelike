from roguelike.model.character import Character
from roguelike.model.world.world import World

class Player(Character):
    def __init__(self, world: World):
        super().__init__(world)

    def move(self, x, y):
        if self.occupied_tile is not None:
            self.occupied_tile.leave()
        self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)

