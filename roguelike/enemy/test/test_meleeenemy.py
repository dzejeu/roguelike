from roguelike.enemy.meleeenemy import DumbMeleeEnemy
from roguelike.model.world.world import World
from roguelike.model.player import Player
from roguelike.model.character import MovingDirections
from unittest import TestCase

class TestMeleeEnemy(TestCase):

    def test_if_best_move_will_be_chosen(self):
        world = World(600, 600)
        player = Player(world)
        enemy = DumbMeleeEnemy(world)
        player.move(10,10)
        enemy.move(0,0)

        tile = enemy.find_best_tile_to_move(player.occupied_tile)

        if tile != (0,1) and tile != (1,0):
            self.fail()

    def test_if_best_move_will_be_chosen_with_obstacle(self):
        world = World(600, 600)
        player = Player(world)
        enemy = DumbMeleeEnemy(world)
        obstacle_player = Player(world)
        obstacle_player.move(1,0)
        player.move(0,10)
        enemy.move(0,0)

        enemy.chase_player(player.occupied_tile)
        self.assertEquals(world.tiles[0][1].occupied_by.__class__, DumbMeleeEnemy)

