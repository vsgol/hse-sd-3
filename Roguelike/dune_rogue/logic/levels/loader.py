import os
from pathlib import Path

from dune_rogue.logic.levels.level import Level


class LevelLoader:
    """Loader for levels"""
    def __init__(self):
        cwd = os.path.realpath(__file__)
        path = Path(cwd)
        self.levels_dir = str(path.parent.absolute()) + os.sep + 'predefined' + os.sep
        self.current_level = 0
        self.number_of_levels = len(os.listdir(self.levels_dir))

    def load_next_from_file(self, player):
        """ Loads next level from file
        :argument player: player character
        :return: next level
        """
        self.current_level += 1
        if self.current_level > self.number_of_levels:
            return None
        return Level(self.levels_dir + f'level_{self.current_level}.lvl', player)

    def reset(self):
        """Start loading levels from the first"""
        self.current_level = 0
