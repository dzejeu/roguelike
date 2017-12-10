import pygame

BASE_ASSET_SIZE = 32


def create_solid_surface(size, color):
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface


class Asset:
    def __init__(self, surface: pygame.Surface, size=(BASE_ASSET_SIZE, BASE_ASSET_SIZE),
                 offset=None, alpha=False):
        self.surface: pygame.Surface = surface
        self.size = size
        self.offset = offset
        self.optimized = False
        self.alpha = alpha

    def draw(self, dest: pygame.Surface, position):
        if not self.optimized:
            self.surface = self.surface.convert_alpha() if self.alpha else self.surface.convert()
            self.optimized = True

        if self.offset is not None:
            position = (position[0] + self.offset[0], position[1] + self.offset[1])

        dest.blit(self.surface, position)


class Assets:
    BASE_ASSET_SIZE = BASE_ASSET_SIZE
    PLAYER_FRONT = Asset(pygame.image.load("assets/player_front.png"), (32, 42), (0, -10), alpha=True)
    PLAYER_BACK = Asset(pygame.image.load("assets/player_back.png"), (32, 42), (0, -10), alpha=True)
    PLAYER_LEFT = Asset(pygame.image.load("assets/player_left.png"), (32, 42), (0, -10), alpha=True)
    PLAYER_RIGHT = Asset(pygame.image.load("assets/player_right.png"), (32, 42), (0, -10), alpha=True)
    DUMB_ENEMY = Asset(pygame.image.load("assets/ghost.png"), alpha=True)
    BOUNDED_ENEMY = Asset(pygame.image.load("assets/skeleton.png"), alpha=True)
    ROOM = Asset(pygame.image.load("assets/room.png"))
    CORRIDOR = Asset(pygame.image.load("assets/room.png"))
    ATTACK = Asset(pygame.image.load('assets/attack.png'), alpha=True)
    WALL = Asset(create_solid_surface((BASE_ASSET_SIZE, BASE_ASSET_SIZE), (63, 66, 76)))
    GOLD = Asset(pygame.image.load('assets/gold.png'), (16, 16), (10, 10), alpha=True)
    ENEMY_ATTACK = Asset(pygame.image.load('assets/enemy_attack.png'), (12, 12), (-5, -5), alpha=True)
    SHIELD = Asset(pygame.image.load('assets/shield.png'), (16, 16), (10, 10), alpha=True)
    SWORD = Asset(pygame.image.load('assets/sword.png'), (16, 16), (10, 10), alpha=True)

