import os
from shutil import copyfile

import pygame

from roguelike.controller import Controller
from roguelike.controller import inputmap
from roguelike.enemy import BaseEnemy
from roguelike.enemy.meleeenemy import DumbMeleeEnemy, BoundedEnemy
from roguelike.model import World
from roguelike.model.player import Player
from roguelike.view import View
from roguelike.model.world.level import Level
from roguelike.model.world.skill import Skill
enemies = []
all_characters = []
visited_rooms = []
obj_no = 0
room_no = 0
level_no = 0
enemy_no = 0

def next_level(world,player,controller):
    controller.draw_text("Wait, level is being generated!")
    pygame.event.set_allowed(None)
    global obj_no
    global room_no
    global all_characters
    global enemies
    global visited_rooms
    global level_no
    global enemy_no
    if level_no<10:
        level = Level(level_no)
        obj_no = level.obj_no
        room_no=level.room_count[level_no]
        enemy_no=level.a_count[level_no]+level.b_count[level_no]+level.c_count[level_no]
        all_characters=[]
        enemies=[]
        visited_rooms=[]
        world.gen_level(room_no, True, level.random_connections_count[level_no])
        player.spawn()
        all_characters.append(player)
        for enemy in range(level.a_count[level_no]):
            easy_enemy = DumbMeleeEnemy(world)
            easy_enemy.spawn_random()
            enemies.append(easy_enemy)
            all_characters.append(easy_enemy)

        for enemy in range(level.c_count[level_no]):
            smarter_enemy = BoundedEnemy(world)
            smarter_enemy.spawn_random()
            enemies.append(smarter_enemy)
            all_characters.append(smarter_enemy)

        chase_enemy = pygame.USEREVENT + 1
        check_for_attack = pygame.USEREVENT + 2
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, chase_enemy, check_for_attack])
        controller.draw_text("")
    else:
        pygame.event.set_allowed([pygame.QUIT])
        world.gen_level(10, True, 5)
        player.spawn()
        all_characters.append(player)
        pygame.mixer.music.stop()


def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    world_width = 200
    world_height = 100

    screen_width = 800
    screen_height = 600


    global obj_no
    global room_no
    global all_characters
    global enemies
    global visited_rooms
    global level_no
    global enemy_no

    input_conf_file = os.path.join(os.path.dirname(__file__), 'input.conf')
    if not os.path.exists(input_conf_file):
        copyfile(input_conf_file + ".default", input_conf_file)

    pygame.key.set_repeat(1, 120)
    chase_enemy = pygame.USEREVENT + 1
    check_if_alived = pygame.USEREVENT + 2
    pygame.time.set_timer(chase_enemy, 450)
    pygame.time.set_timer(check_if_alived, 300)
    # set_allowed(None) blokuje wszystkie i jest niezbedne zeby pozniej uaktywnic tylko niektore
    # pygame -.-
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, chase_enemy, check_if_alived])

    world = World(world_width, world_height)
    player = Player(world)
    view = View(world, screen_width, screen_height, player)
    controller = Controller(player, view)

    next_level(world,player,controller)
    skill = Skill(player)
    pygame.mixer.music.load('sound/bgsound.mp3')
    pygame.mixer.music.play(-1)

    with open(input_conf_file, 'r') as f:
        controller.input_map = inputmap.load(f)

    while controller.running:
        if level_no > 9:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    controller.process_input(event.key)
                controller.win_view()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    controller.process_input(event.key)
                    if obj_no == 2:
                        xy = player.occupied_tile.get_position()
                        r_no = world.get_room(xy[0],xy[1])
                        if not visited_rooms.__contains__(r_no) and r_no!=-1:
                            visited_rooms.append(r_no)
                            if len(visited_rooms)==room_no:
                                level_no=level_no+1
                                next_level(world, player,controller)
                                skill.improve(level_no)
                    elif obj_no == 1:
                        if len(enemies)==0:
                            level_no = level_no + 1
                            next_level(world, player,controller)
                            skill.improve(level_no)
                    elif obj_no == 3:
                        if len(enemies)==0:
                            level_no = level_no + 1
                            next_level(world, player,controller)
                            skill.improve(level_no)
                        if player.gold >= enemy_no*3:
                            level_no = level_no + 1
                            next_level(world, player,controller)
                            skill.improve(level_no)
                if event.type == chase_enemy:
                    for enemy in enemies:
                        enemy.chase_player(player.occupied_tile)
                if event.type == check_if_alived:
                    for char in all_characters:
                        if not char.check_if_alived():
                            all_characters.remove(char)
                            if issubclass(char.__class__, BaseEnemy):
                                enemies.remove(char)
                controller.update_view()
                pygame.time.wait(20)
    pygame.quit()


main()
