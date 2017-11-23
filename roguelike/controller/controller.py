from typing import Dict
import pygame

from roguelike.controller.commands import Command
from roguelike.model.character import MovingDirections
from roguelike.model.player import Player
from roguelike.view import View


class Controller:
    def __init__(self, player: Player, view: View):
        self.player = player
        self.running: bool = True
        self.view: View = view
        self.input_map: Dict[int, Command] = dict()

    def process_input(self, key):
        command = self.input_map.get(key)
        if command is not None:
            self.run_command(command)

    def run_command(self, command: Command):
        if command == Command.QUIT:
            self.running = False
        elif command == Command.MOVE_UP:
            direction = MovingDirections.UP.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
        elif command == Command.MOVE_DOWN:
            direction = MovingDirections.DOWN.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
        elif command == Command.MOVE_RIGHT:
            direction = MovingDirections.RIGHT.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
        elif command == Command.MOVE_LEFT:
            direction = MovingDirections.LEFT.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
        elif command == Command.ATTACK_UP:
            direction = MovingDirections.UP.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
        elif command == Command.ATTACK_LEFT:
            direction = MovingDirections.LEFT.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
        elif command == Command.ATTACK_DOWN:
            direction = MovingDirections.DOWN.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
        elif command == Command.ATTACK_RIGHT:
            direction = MovingDirections.RIGHT.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)

    def update_view(self):
        self.view.draw(self.player)
