from roguelike.enemy.meleeenemy import EasyMeleeEnemy
from roguelike.model.world.world import World
from roguelike.model.player import Player
from roguelike.model.character import MovingDirections
from unittest import TestCase

class TestMeleeEnemy(TestCase):

    def test_if_best_move_will_be_chosen(self):
        world = World(600, 600)
        player = Player(world)
        enemy = EasyMeleeEnemy(world)
        player.move(10,10)
        enemy.move(0,0)

        direction = enemy.find_best_direction_to_move(player.occupied_tile)

        self.assertEquals(direction, MovingDirections.DOWN_RIGHT)

    def test_if_best_move_will_be_chosen_with_obstacle(self):
        world = World(600, 600)
        player = Player(world)
        enemy = EasyMeleeEnemy(world)
        obstacle_player = Player(world)
        obstacle_player.move(1,0)
        player.move(0,10)
        enemy.move(0,0)

        direction = enemy.chase_player(player.occupied_tile)

        self.assertEquals(world.tiles[1][1].occupying_class, EasyMeleeEnemy)