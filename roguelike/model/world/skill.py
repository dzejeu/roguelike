from roguelike.model.player import Player
from math import log2

class Skill:
    def __init__(self, player):
        self.Player = player

    def improve(self, level):
        self.Player.max_hp = (log2(self.Player.max_hp)*0.4*level)+self.Player.max_hp
        self.Player.base_attack = (log2(self.Player.base_attack)*0.4*level)+self.Player.base_attack
        self.Player.base_defense = (log2(self.Player.base_defense)*0.4*level)+self.Player.base_defense
        self.Player.hp = self.Player.max_hp
