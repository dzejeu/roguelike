import math

from roguelike.model import character

class PathNotFound(Exception):
    pass

def get_adjacent_reachable_tiles(current, world):
    reachable_tiles = []
    for dir in character.MovingDirections:
        new_x = current.x + dir.value.x
        new_y = current.y + dir.value.y
        if any((new_x, new_y)) < 0 or new_x >= world.width or new_y >= world.height:
            continue
        else:
            if world.tiles[new_x][new_y].passable and (
                            world.tiles[new_x][new_y].type == "R" or world.tiles[new_x][new_y].type == "C"):
                reachable_tiles.append(world.tiles[new_x][new_y])
    return reachable_tiles


def heuristic_cost_estimate(start_tile, end_tile):
    return math.sqrt(math.pow(float(start_tile.x - end_tile.x), 2) + math.pow(float(start_tile.y - start_tile.x), 2))

def reconstruct_path(came_from, current):
    path = [current,]
    while current in came_from.keys():
        current = came_from[current]
        path.append(current)
    return path

def A_star_pathfinding(start_tile, end_tile, world):
    world_map = [world.tiles[x][y] for x in range(world.width) for y in range(world.height)]
    already_evaluated = set()
    open_set = {start_tile}
    came_from = {}
    gScore = {tile: math.inf for tile in world_map}
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

            if neighbour not in open_set:
                open_set.add(neighbour)

            score = gScore[current] + heuristic_cost_estimate(current, neighbour)
            if score >= gScore[neighbour]:
                continue

            came_from[neighbour] = current
            gScore[neighbour] = score
            fScore[neighbour] = gScore[neighbour] + heuristic_cost_estimate(neighbour, end_tile)

    raise PathNotFound()
