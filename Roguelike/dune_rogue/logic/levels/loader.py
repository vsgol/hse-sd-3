import os
from pathlib import Path

from dune_rogue.logic.levels.level import Level
from dune_rogue.logic.entities.factory import EntityFactory


class LevelLoader:
    """Loader for levels"""
    def __init__(self):
        cwd = os.path.realpath(__file__)
        path = Path(cwd)
        self.levels_dir = str(path.parent.absolute()) + os.sep + 'predefined' + os.sep
        self.current_level = 0

    def load_next_from_file(self, player):
        """ Loads next level from file
        :argument player: player character
        :return: next level
        """
        self.current_level += 1
        return Level(self.levels_dir + f'level_{self.current_level}.lvl', player)


if __name__ == '__main__':
    loader = LevelLoader()
    lvl = loader.load_next_from_file(EntityFactory.create_player_character(0, 0))
    txt, _ = lvl.render()
    print(txt)
