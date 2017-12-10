import math
from heapq import *
from roguelike.model import character
from roguelike.model import player
import numpy as np

class PathNotFound(Exception):
    pass


def get_adjacent_reachable_tiles(current, world):
    reachable_tiles = []
    for dir in character.MovingDirections:
        if world.tiles.__class__ == np.ndarray:
            new_x = np.where(world.tiles == current)[0][0] + dir.value.x
            new_y = np.where(world.tiles == current)[1][0] + dir.value.y
        else:
            new_x = current.x + dir.value.x
            new_y = current.y + dir.value.y
        if any((new_x, new_y)) < 0 or new_x >= world.width or new_y >= world.height:
            continue
        else:
            try:
                if (world.tiles[new_x][new_y].passable and (
                        world.tiles[new_x][new_y].type == "R" or world.tiles[new_x][new_y].type == "C")) or \
                                world.tiles[new_x][new_y].occupied_by.__class__ == player.Player:
                    reachable_tiles.append(world.tiles[new_x][new_y])
            except IndexError:
                continue
    return reachable_tiles


def get_euclidean_distance(tile1, tile2):
    return math.sqrt(pow(float(tile1.x - tile2.x), 2) + pow(float(tile1.y - tile2.y), 2))


def get_manhattan_distance(tile1, tile2):
    return abs(tile1.x - tile2.x) + abs(tile1.y - tile2.y)


def heuristic_cost_estimate(start_tile, end_tile):
    return get_manhattan_distance(start_tile, end_tile)


def reconstruct_path(came_from, current):
    path = [current, ]
    while current in came_from.keys():
        current = came_from[current]
        path.append(current)
    return path


def A_star_pathfinding(start_tile, end_tile, world):
    already_evaluated = set()
    open_set = {start_tile}
    came_from = {}
    gScore = {world.tiles[x][y]: math.inf for x in range(world.width) for y in range(world.height)}
    fScore = gScore.copy()
    gScore[start_tile] = 0
    fScore[start_tile] = heuristic_cost_estimate(start_tile, end_tile)
    while open_set:
        current = min(open_set, key=lambda x: fScore[x])
        if current == end_tile:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        already_evaluated.add(current)

        for neighbour in get_adjacent_reachable_tiles(current, world):
            if neighbour in already_evaluated:
                continue

            score = gScore[current] + heuristic_cost_estimate(current, neighbour)
            if score >= gScore[neighbour]:
                continue

            if neighbour not in open_set:
                came_from[neighbour] = current
                gScore[neighbour] = score
                fScore[neighbour] = gScore[neighbour] + heuristic_cost_estimate(neighbour, end_tile)
                open_set.add(neighbour)

    raise PathNotFound()
