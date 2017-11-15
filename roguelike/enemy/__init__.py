from roguelike.model.character import Character

class BaseEnemy(Character):

    def find_best_tile_to_move(self, target_tile):
        raise NotImplemented()
