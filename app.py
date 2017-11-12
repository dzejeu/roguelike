import pygame

from roguelike.view import View
from roguelike.controller import Controller
from roguelike.model import World


def main():
    pygame.init()
    world_width = 100
    world_height = 100

    world = World(world_width, world_height)
    world.gen_level(10, True, 2)

    view = View(world)
    controller = Controller(world, view)

    while controller.running:
        controller.process_input()
        controller.update_view()

    pygame.quit()


main()
