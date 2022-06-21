from enum import Enum


class State(Enum):
    """Game state enumeration"""
    LEVEL = 1
    INVENTORY = 2
    PAUSE_MENU = 3
    MAIN_MENU = 4
    LEVEL_SELECTION = 5
    SAVE = 6
    LOAD = 7
    EXIT = 8
    ERR = 9
    DUNGEON = 10
    SWITCH_VISION = 11