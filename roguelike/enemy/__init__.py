from roguelike.model.character import Character

class BaseEnemy(Character):

    def find_best_direction_to_move(self, target_tile):
        raise NotImplemented()


