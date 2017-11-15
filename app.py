import os
import pygame

from roguelike.controller import inputmap
from roguelike.view import View
from roguelike.controller import Controller
from roguelike.model import World


def main():
    pygame.init()
    world_width = 100
    world_height = 100
    input_conf_file = os.path.join(os.path.dirname(__file__), 'input.conf')

    world = World(world_width, world_height)
    world.gen_level(10, True, 2)

    view = View(world)
    controller = Controller(world, view)

    with open(input_conf_file, 'r') as f:
        controller.input_map = inputmap.load(f)

    while controller.running:
        controller.process_input()
        controller.update_view()

    pygame.quit()


main()
