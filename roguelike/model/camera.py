# Camera
import pygame

class Camera():
    def __init__(self, map_width, map_height, screen_width, screen_height):
        """
        Class for camera scrolling.
        :param map_width: size the map in pixel
        :param map_height: size the map in pixel
        """
        self.state = pygame.Rect(0, 0, map_width, map_height)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, player_position):
        """
        :param player: player object
        Update camera's state to follow player.
        """
        self.state = self.calc_camera(player_position)

    def apply(self):
        """
        Move and return entity on the screen.
        :param target: entity e.g. tile, player, enemy
        :return:
        """
        return (self.state.x, self.state.y)

    def calc_camera(self, player_position):
        """
        :param player_direction: position of the player on the map. pygame.Rect()
        :return: calc the state of the camera, so that the player is in the center of the screen
        """
        l, t, _, _ = player_position
        _, _, w, h = self.state
        l, t, _, _ = -l + self.screen_width / 2, -t + self.screen_height / 2, w, h  # center player

        l = min(0, l)  # stop scrolling at the left edge
        l = max(-(self.state.width - self.screen_width), l)  # stop scrolling at the right edge
        t = max(-(self.state.height - self.screen_height), t)  # stop scrolling at the bottom
        t = min(0, t)  # stop scrolling at the top

        return pygame.Rect(l, t, w, h)
