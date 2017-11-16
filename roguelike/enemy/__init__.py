from roguelike.model.character import Character
import random


class BaseEnemy(Character):

    def find_best_tile_to_move(self, target_tile):
        raise NotImplemented()

    def spawn_random(self):
        all_tiles = [self.world.tiles[w][h] for w in range(self.world.width) for h in range(self.world.height)]
        available_tiles = list(filter(lambda x: x.occupying_class is None and x.type=='R', all_tiles))
        [random_tile]= random.sample(available_tiles, 1)
        self.move(random_tile.x, random_tile.y)