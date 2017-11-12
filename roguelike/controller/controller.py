import pygame

from roguelike.model import World
from roguelike.view import View


class Controller:
    def __init__(self, world: World, view: View):
        self.running: bool = True
        self.world: World = world
        self.view: View = view

    def process_input(self):
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            self.running = False

    def update_view(self):
        self.view.draw()
