import unittest

from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.levels.loader import LevelLoader


class LvlLoaderTest(unittest.TestCase):
    def test_loading(self):
        loader = LevelLoader()
        self.assertEqual(loader.current_level, 0)
        loader.load_next_from_file(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)

    def test_reset(self):
        loader = LevelLoader()
        self.assertEqual(loader.current_level, 0)
        loader.load_next_from_file(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)
        loader.reset()
        self.assertEqual(loader.current_level, 0)
        loader.load_next_from_file(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)

if __name__ == '__main__':
    unittest.main()
