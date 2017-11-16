from roguelike.model.character import Character
from roguelike.model.world.world import World

class Player(Character):
    def __init__(self, world: World):
        super().__init__(world)

    def spawn_random(self):
        #todo: refactor this ugly shiet
        found = False
        for h in range(self.world.height):
            for w in range(self.world.width):
                if self.world.tiles[w][h].type == "R" and self.world.tiles[w][h].occupying_class is None:
                    self.move(w, h)
                    found = True
                    break
            else:
                continue
            if found:
                break

    def move(self, x, y):
        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.world.tiles[x][y].passable:
                if self.occupied_tile is not None:
                    self.occupied_tile.leave()
                self.occupied_tile = self.world.tiles[x][y].occupy(self.__class__)

