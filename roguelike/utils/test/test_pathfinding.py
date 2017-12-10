from time import time

from roguelike.model.world.world import World
from roguelike.model.world.tile import Tile
from roguelike.utils.pathfinding import A_star_pathfinding, PathNotFound
#
# def test_if_A_star_pathfinding_returns_path_when_no_obstacles_present():
#     world = World(100, 100, default_tile_type='R')
#     path = A_star_pathfinding(world.tiles[2][3], world.tiles[30][23], world)
#     if not path:
#         raise Exception('Path is empty')
#
#
# def test_if_A_star_pathfinding_raise_exception_when_no_path_can_be_found():
#     world = World(20, 20, default_tile_type='R')
#     # split map into 2 pieces with obstacle
#     for y in range(world.height):
#         world.tiles[10][y].type = 'V'
#     try:
#         path = A_star_pathfinding(world.tiles[2][3], world.tiles[15][3], world)
#     except PathNotFound:
#         return


def find_path():
    world = World(30, 30, default_tile_type='R')
    A_star_pathfinding(world.tiles[2][3], world.tiles[23][27], world)
    return

times = []
for i in range(1):
    start = time()
    find_path()
    times.append(time() - start)

print(sum(times) / len(times))