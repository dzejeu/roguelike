from roguelike.enemy.meleeenemy import DumbMeleeEnemy
from roguelike.model.character import Character
from roguelike.model.world.world import World

class Player(Character):
    def __init__(self, world: World):
        super().__init__(world)

    def spawn(self):
        spawn_room = self.world.room_list[0]
        spawn_x = int(spawn_room[2]+spawn_room[0]/2)
        spawn_y = int(spawn_room[3]+spawn_room[1]/2)
        self.move(spawn_x,spawn_y)

    def check_for_attack(self):
        if self.occupied_tile.mark_as_attacked > 0:
            self.on_damage(80)
            self.occupied_tile.mark_as_attacked = 0

    def move(self, x, y):
        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.world.tiles[x][y].passable:
                if self.occupied_tile is not None:
                    self.occupied_tile.leave()
                self.occupied_tile = self.world.tiles[x][y].occupy(self)

    def attack(self,x ,y):
        if self.world.tiles[x][y].occupied_by.__class__ == DumbMeleeEnemy:
            self.world.tiles[x][y].mark_as_attacked = 20
        else:
            self.world.tiles[x][y].mark_as_attacked = 10