import pygame

from roguelike.model.menuoption import MenuOption


class Shop:
    def __init__(self, player, name):
        self.name = name
        self.player = player
        self.options = [
            MenuOption("apteczka (+20hp) - 20g", self.buy, {"price": 20, "callback": self.first_aid}),
            MenuOption("miecz (+10%) - 50g", self.buy, {"price": 50, "callback": self.sword}),
            MenuOption("helm (+5%) - 40g", self.buy, {"price": 40, "callback": self.helmet}),
            MenuOption("napiersnik (+10%) - 80g", self.buy, {"price": 80, "callback": self.breastplate}),
            MenuOption("rekawice (+3%) - 30g", self.buy, {"price": 30, "callback": self.gloves}),
            MenuOption("buty (+4%) - 35g", self.buy, {"price": 30, "callback": self.boots}),
        ]

    def buy(self, price, callback):
        if self.player.gold >= price:
            self.player.gold -= price
            effect = pygame.mixer.Sound('sound/register.ogg')
            effect.set_volume(0.1)
            effect.play()
            callback()

    def first_aid(self):
        self.player.hp = max(self.player.max_hp, self.player.hp + 20)

    def sword(self):
        self.player.base_attack *= 1.1

    def helmet(self):
        self.player.base_defense *= 1.05

    def breastplate(self):
        self.player.base_defense *= 1.1

    def gloves(self):
        self.player.base_defense *= 1.03

    def boots(self):
        self.player.base_defense *= 1.04

    def select_option(self, idx):
        if idx < len(self.options):
            item = self.options[idx]
            item.callback(**item.args)

    def available(self, idx):
        if idx < len(self.options):
            item = self.options[idx]
            if self.player.gold >= item.args["price"]:
                return True

        return False
