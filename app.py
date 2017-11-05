import pygame

from roguelike.model.world import World


def main():
    pygame.init()
    world_width = 100
    world_height = 100
    world = World(world_width,world_height)
    surface_width = 8*world.width
    surface_height = 8*world.height

    main_surface = pygame.display.set_mode((surface_width, surface_height))

    world.gen_level(10, True, 2)

    room_color = (255, 255, 255)
    wall_color = (255,0,0)

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break

        main_surface.fill((0, 0, 0))

        for i in range(world_width):
            for j in range(world_height):
                tile = (i*8,j*8,8,8)
                if (world.tiles[i][j].type == "R"):
                    main_surface.fill(room_color, tile)
                if (world.tiles[i][j].type == "W"):
                    main_surface.fill(wall_color, tile)
                if(world.tiles[i][j].type == "C"):
                    main_surface.fill(room_color, tile)
        pygame.display.flip()

    pygame.quit()

main()