from model.entity import Entity


class BaseTile:
    breakable = False
    collidable = False
    passable = True

    def __init__(self):
        pass

    def on_collision(self, other: Entity):
        pass
