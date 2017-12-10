from roguelike.enemy import BaseEnemy
from roguelike.enemy.meleeenemy import DumbMeleeEnemy
from roguelike.model.character import Character, MovingDirections
from roguelike.model.world.world import World

class Player(Character):
    def __init__(self, world: World):
        super().__init__(world)
        self.base_attack = 300
        self.base_defense = 100

    def spawn(self):
        spawn_room = self.world.room_list[0]
        spawn_x = int(spawn_room[2]+spawn_room[0]/2)
        spawn_y = int(spawn_room[3]+spawn_room[1]/2)
        self.move(spawn_x,spawn_y)

    def move(self, x, y):
        if self.occupied_tile is not None:
            self.looking_direction = MovingDirections.get_direction_from_diff(
                (self.occupied_tile.x, self.occupied_tile.y), (x, y))

        if self.world.tiles[x][y].type == "R" or self.world.tiles[x][y].type == "C":
            if self.world.tiles[x][y].passable:
                if self.occupied_tile is not None:
                    self.occupied_tile.leave()
                self.occupied_tile = self.world.tiles[x][y].occupy(self)

    def attack(self,x ,y):
        self.looking_direction = MovingDirections.get_direction_from_diff(
            (self.occupied_tile.x, self.occupied_tile.y), (x, y))
        if issubclass(self.world.tiles[x][y].occupied_by.__class__, BaseEnemy):
            self.world.tiles[x][y].mark_as_attacked = 8
            self.world.tiles[x][y].occupied_by.on_damage(self.base_attack)
        else:
            self.world.tiles[x][y].mark_as_attacked = 6

    def check_if_alived(self):
        if self.hp == 0:
            pass    #TODO: loose screen

