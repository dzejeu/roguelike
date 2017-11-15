from typing import Dict
import pygame

from roguelike.model.character import MovingDirections
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
        print("Command: {}".format(command))
        if command == Command.QUIT:
            self.running = False
        elif command == Command.MOVE_UP:
            direction = MovingDirections.UP.value
            self.world.player.move(self.world.player.position.x + direction.x,
                                   self.world.player.position.y + direction.y)
        elif command == Command.MOVE_DOWN:
            direction = MovingDirections.DOWN.value
            self.world.player.move(self.world.player.position.x + direction.x,
                                   self.world.player.position.y + direction.y)
        elif command == Command.MOVE_RIGHT:
            direction = MovingDirections.RIGHT.value
            self.world.player.move(self.world.player.position.x + direction.x,
                                   self.world.player.position.y + direction.y)
        elif command == Command.MOVE_LEFT:
            direction = MovingDirections.LEFT.value
            self.world.player.move(self.world.player.position.x + direction.x,
                                   self.world.player.position.y + direction.y)

    def update_view(self):
        self.view.draw()
