import unittest

from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.levels.loader import LevelLoader, LevelGenerator


class LvlLoaderTest(unittest.TestCase):
    def test_loading(self):
        loader = LevelLoader()
        self.assertEqual(loader.current_level, 0)
        loader.build(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)

    def test_reset(self):
        loader = LevelLoader()
        self.assertEqual(loader.current_level, 0)
        loader.build(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)
        loader.reset()
        self.assertEqual(loader.current_level, 0)
        loader.build(PlayerCharacter(0, 0))
        self.assertEqual(loader.current_level, 1)

    def test_many_gen(self):
        N_GENS = 1000
        loader = LevelGenerator()
        for i in range(N_GENS):
            loader.set_sizes(30, 30)
            loader.build(PlayerCharacter(0, 0))


if __name__ == '__main__':
    unittest.main()
