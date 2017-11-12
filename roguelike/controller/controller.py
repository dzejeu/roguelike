from typing import Dict
import pygame

from roguelike.controller.commands import Command
from roguelike.model import World
from roguelike.view import View


class Controller:
    def __init__(self, world: World, view: View):
        self.running: bool = True
        self.world: World = world
        self.view: View = view
        self.input_map: Dict[int, Command] = dict()

    def process_input(self):
        ev = pygame.event.poll()

        if ev.type == pygame.QUIT:
            self.run_command(Command.QUIT)
        elif ev.type == pygame.KEYDOWN:
            command = self.input_map.get(ev.key)

            if command is not None:
                self.run_command(command)

    def run_command(self, command: Command):
        if command == Command.QUIT:
            self.running = False

    def update_view(self):
        self.view.draw()
