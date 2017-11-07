# Camera
import pygame
from roguelike.model.world import World

## need size of the map in pixel
screen_width = World.screen_width
screen_height = World.screen_height

class Camera():
    """
    Class for camera scrolling.
    :param map_width: size the map in pixel
    :param map_height: size the map in pixel

    Usage:
    camera = Camera(total_level_width, total_level_height)
    camera.update(player) # camera follows player
    ...
    entities.add(player)

    for l in level: ??
        entities.add(l) ??

    while True:

        for e in pygame.event.get():
            ...
        ...
        ...
        # update player, draw everything else
        camera.update(player) 
        player.move(...)

        for e in entities:
            # apply the offset to each entity.
            # call this for everything that should scroll,
            # which is basically everything
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
    """
    def __init__(self, map_width, map_height):
        self.state = pygame.Rect(0, 0, map_width, map_height)

    def update(self, player):
        """
        :param player: player object
        Update camera's state to follow player.
        player.direction is pygame.Rect(x,y, width_player_image, height_player_image)
        """
        self.state = self.calc_camera(player.direction)

    def apply(self, target):
        """
        Move and return entity on the screen.
        :param target: entity e.g. tile, player, enemy
        :return:
        """
        return target.direction.move(self.state.topleft)

    def calc_camera(self, player_direction):
        """
        :param player_direction: position of the player on the map. pygame.Rect()
        :return: calc the state of the camera, so that the player is in the center of the screen
        """
        l, t, _, _ = player_direction
        _, _, w, h = self.state
        l, t, _, _ = -l + screen_width / 2, -t + screen_height / 2, w, h  # center player

        l = min(0, l)  # stop scrolling at the left edge
        l = max(-(self.state.width - screen_width), l)  # stop scrolling at the right edge
        t = max(-(self.state.height - screen_height), t)  # stop scrolling at the bottom
        t = min(0, t)  # stop scrolling at the top

        return pygame.Rect(l, t, w, h)
