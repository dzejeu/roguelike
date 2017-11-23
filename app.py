import os
from shutil import copyfile

import pygame

from roguelike.controller import Controller
from roguelike.controller import inputmap
from roguelike.enemy.meleeenemy import DumbMeleeEnemy, BoundedEnemy
from roguelike.model import World
from roguelike.model.player import Player
from roguelike.view import View


def main():
    pygame.init()
    world_width = 200
    world_height = 100

    screen_width = 800
    screen_height = 600

    input_conf_file = os.path.join(os.path.dirname(__file__), 'input.conf')
    if not os.path.exists(input_conf_file):
        copyfile(input_conf_file + ".default", input_conf_file)

    pygame.key.set_repeat(1, 100)
    chase_enemy = pygame.USEREVENT + 1
    check_for_attack = pygame.USEREVENT + 2
    pygame.time.set_timer(chase_enemy, 500)
    pygame.time.set_timer(check_for_attack, 100)
    # set_allowed(None) blokuje wszystkie i jest niezbedne zeby pozniej uaktywnic tylko niektore
    # pygame -.-
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, chase_enemy, check_for_attack])

    world = World(world_width, world_height)
    world.gen_level(10, True, 2)
    player = Player(world)
    view = View(world, screen_width, screen_height, player)
    controller = Controller(player, view)
    enemies = []
    all_characters = []

    with open(input_conf_file, 'r') as f:
        controller.input_map = inputmap.load(f)

    player.spawn()
    all_characters.append(player)
    for enemy in range(10):
        easy_enemy = DumbMeleeEnemy(world)
        easy_enemy.spawn_random()
        enemies.append(easy_enemy)
        all_characters.append(easy_enemy)

    # for enemy in range(1):
    #     bounded_enemy = BoundedEnemy(world)
    #     bounded_enemy.spawn_random()
    #     enemies.append(bounded_enemy)

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
            if event.type == check_for_attack:
                for char in all_characters:
                    char.check_for_attack()
            controller.update_view()
            pygame.time.wait(20)
    pygame.quit()


main()
