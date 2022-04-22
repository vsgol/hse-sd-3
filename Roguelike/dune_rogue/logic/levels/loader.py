import os
from abc import ABC
from pathlib import Path

from dune_rogue.logic.levels.level import Level


class LevelBuilder(ABC):
    def __init__(self):
        self.factory = None

    """Abstract level builder class"""
    def set_sizes(self, w, h):
        """Set level sized before build"""
        pass

    def build(self, player):
        """Builds level"""
        raise NotImplementedError('build is not implemented')

    def reset(self):
        """Resets builder"""
        pass

    def set_factory(self, factory):
        """Sets factory for levels building"""
        self.factory = factory


class LevelLoader(LevelBuilder):
    """Loader for levels"""
    def __init__(self):
        super().__init__()
        cwd = os.path.realpath(__file__)
        path = Path(cwd)
        self.levels_dir = str(path.parent.absolute()) + os.sep + 'predefined' + os.sep
        self.current_level = 0
        self.number_of_levels = len(os.listdir(self.levels_dir))

    def build(self, player):
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


class LevelGenerator(LevelBuilder):
    def __init__(self):
        super().__init__()
        self.w = None
        self.h = None

    def build(self, player):
        if not self.w or not self.h:
            raise ValueError('width and height must be set before generating level')

        level = Level(None, player)
        level.generate(self.w, self.h, self.factory)

        self.w = None
        self.h = None

        return level

    def set_sizes(self, w, h):
        if w <= 0 or h <= 0:
            raise ValueError('width and height must be positive')
        # + 1 because of edges
        self.w = int(w) + 1
        self.h = int(h) + 1
