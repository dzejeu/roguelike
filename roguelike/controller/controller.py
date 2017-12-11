from typing import Dict
import pygame

from roguelike.controller.commands import Command
from roguelike.model.character import MovingDirections
from roguelike.model.player import Player
from roguelike.view import View
from roguelike.model.shop import Shop
from roguelike.view.menu import Menu


class Controller:
    def __init__(self, player: Player, view: View):
        self.player = player
        self.running: bool = True
        self.view: View = view
        self.input_map: Dict[int, Command] = dict()
        self.menu = None
        self.shop = Menu(Shop(player, "SKLEP"), self.view.main_surface, player)
        self.menu_options = [getattr(Command, "OPTION_{}".format(i)) for i in range(1, 10)]
        self.menu_options.append(Command.OPTION_0)

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
            effect = pygame.mixer.Sound('sound/footsteps.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.MOVE_DOWN:
            direction = MovingDirections.DOWN.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/footsteps.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.MOVE_RIGHT:
            direction = MovingDirections.RIGHT.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/footsteps.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.MOVE_LEFT:
            direction = MovingDirections.LEFT.value
            self.player.move(self.player.occupied_tile.x + direction.x,
                                   self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/footsteps.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.ATTACK_UP:
            direction = MovingDirections.UP.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/attack.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.ATTACK_LEFT:
            direction = MovingDirections.LEFT.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/attack.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.ATTACK_DOWN:
            direction = MovingDirections.DOWN.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/attack.wav')
            effect.set_volume(0.1)
            effect.play()
        elif command == Command.ATTACK_RIGHT:
            direction = MovingDirections.RIGHT.value
            self.player.attack(self.player.occupied_tile.x + direction.x,
                               self.player.occupied_tile.y + direction.y)
            effect = pygame.mixer.Sound('sound/attack.wav')
            effect.set_volume(0.1)
            effect.play()

        elif command == Command.SHOP_TOGGLE:
            if self.menu is None:
                self.menu = self.shop
                self.view.menu = self.shop
            elif self.menu is self.shop:
                self.menu = None
                self.view.menu = None
        elif command in self.menu_options:
            if self.menu is not None:
                i = self.menu_options.index(command)
                self.menu.data.select_option(i)



    def update_view(self):
        self.view.draw(self.player)
    def win_view(self):
        self.view.draw_win_text()
    def lose_view(self):
        self.view.draw_lose_text()
    def draw_text(self,t):
        self.view.draw_text(t)
