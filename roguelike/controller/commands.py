from enum import Enum, auto


class Command(Enum):
    QUIT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    ATTACK_UP = auto()
    ATTACK_LEFT = auto()
    ATTACK_DOWN = auto()
    ATTACK_RIGHT = auto()
