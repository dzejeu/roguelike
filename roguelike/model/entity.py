class Entity(object):
    def on_collision(self, other: 'Entity'):
        pass

    def on_damage(self, damage: int):
        pass
