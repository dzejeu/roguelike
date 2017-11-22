import pygame

BASE_ASSET_SIZE = 32


def create_solid_surface(size, color):
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface


class Asset:
    def __init__(self, surface: pygame.Surface, size = (BASE_ASSET_SIZE, BASE_ASSET_SIZE),
                 offset = None, alpha = False):
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
    PLAYER = Asset(pygame.image.load("assets/player_right.png"), (32, 42), (0, -10), alpha=True)
    DUMB_ENEMY = Asset(pygame.image.load("assets/ghost.png"), alpha=True)
    ROOM = Asset(pygame.image.load("assets/room.png"))
    CORRIDOR = Asset(pygame.image.load("assets/room.png"))
    WALL = Asset(create_solid_surface((BASE_ASSET_SIZE, BASE_ASSET_SIZE), (63, 66, 76)))
