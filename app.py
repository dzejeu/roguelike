import os
import pygame

from roguelike.controller import inputmap
from roguelike.view import View
from roguelike.controller import Controller
from roguelike.model import World
from roguelike.model.player import Player


def main():
    pygame.init()
    world_width = 100
    world_height = 100
    input_conf_file = os.path.join(os.path.dirname(__file__), 'input.conf')

    world = World(world_width, world_height)
    world.gen_level(10, True, 2)

    view = View(world)
    world.player = Player(world)
    controller = Controller(world, view)

    with open(input_conf_file, 'r') as f:
        controller.input_map = inputmap.load(f)

    for h in range(world_height):
        for w in range(world_width):
            if world.tiles[w][h].type == "R":
                world.player.move(w, h)
                break
        else:
            continue
        break

    while controller.running:
        controller.process_input()
        controller.update_view()

    pygame.quit()


main()
