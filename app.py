import os
from shutil import copyfile

import pygame

from roguelike.controller import Controller
from roguelike.controller import inputmap
from roguelike.enemy.meleeenemy import DumbMeleeEnemy
from roguelike.model import World
from roguelike.model.player import Player
from roguelike.view import View


def main():
    pygame.init()
    world_width = 300
    world_height = 100

    screen_width = 800
    screen_height = 600

    input_conf_file = os.path.join(os.path.dirname(__file__), 'input.conf')
    if not os.path.exists(input_conf_file):
        copyfile(input_conf_file + ".default", input_conf_file)

    pygame.key.set_repeat(1, 100)
    chase_enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(chase_enemy, 300)
    # set_allowed(None) blokuje wszystkie i jest niezbedne zeby pozniej uaktywnic tylko niektore
    # pygame -.-
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, chase_enemy])

    world = World(world_width, world_height)
    world.gen_level(10, True, 2)
    view = View(world, screen_width, screen_height)
    player = Player(world)
    controller = Controller(player, view)
    enemies = []

    with open(input_conf_file, 'r') as f:
        controller.input_map = inputmap.load(f)

    player.spawn()

    for enemy in range(15):
        easy_enemy = DumbMeleeEnemy(world)
        easy_enemy.spawn_random()
        enemies.append(easy_enemy)

    while controller.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                controller.process_input(event.key)
            if event.type == chase_enemy:
                for enemy in enemies:
                    enemy.chase_player(player.occupied_tile)
            controller.update_view((player.occupied_tile.x, player.occupied_tile.y))
            pygame.time.wait(20)
    pygame.quit()


main()
