from enum import Enum


class Action(Enum):
    """User actions enumeration"""
    # Navigation
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_RIGHT = 3
    MOVE_LEFT = 4
    # Menus
    TOGGLE_INVENTORY = 5
    TOGGLE_PAUSE = 6
    SELECT = 7

