from roguelike.model.character import Character
import random


class BaseEnemy(Character):

    def find_best_tile_to_move(self, target_tile):
        raise NotImplemented()

    def spawn_random(self):
        all_tiles = [self.world.tiles[w][h] for w in range(self.world.width) for h in range(self.world.height)]
        available_tiles = list(filter(lambda x: x.occupied_by is None and x.type=='R', all_tiles))
        [random_tile]= random.sample(available_tiles, 1)
        self.move(random_tile.x, random_tile.y)

    def move(self, x, y):
        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.world.tiles[x][y].passable:
                if self.occupied_tile is not None:
                    self.occupied_tile.leave()
                self.occupied_tile = self.world.tiles[x][y].occupy(self)