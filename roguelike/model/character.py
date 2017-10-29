from .entity import Entity


class Character(Entity):
    def __init__(self):
        self.hp: int = 100
        self.base_defense: int = 10
        self.base_attack: int = 10

    def get_defense(self) -> int:
        return self.base_defense

    def on_damage(self, damage: int):
        self.hp = int(max(0, self.hp - (damage / self.get_defense())))
