from io import TextIOWrapper
from typing import Dict

import pygame
import sys

from roguelike.controller.commands import Command


def load(fp: TextIOWrapper) -> Dict[int, Command]:
    input_map: Dict[int, Command] = dict()
    i = 0
    for line in fp:
        i += 1

        if line.startswith("#"):
            continue

        tokens = line.split()

        if len(tokens) == 2:
            key, command_name, *_ = tokens
            keycode = getattr(pygame, "K_" + key, None)
            command = getattr(Command, command_name.upper(), None)

            if keycode is None:
                print("{}:{}: unknown key \"{}\"".format(fp.name, i, key), file=sys.stderr)
            elif command is None:
                print("{}:{}: unknown command \"{}\"".format(fp.name, i, command_name), file=sys.stderr)
            else:
                input_map[keycode] = command
        elif len(tokens) != 0:
                print("{}:{}: wrong format".format(fp.name, i), file=sys.stderr)

    return input_map
