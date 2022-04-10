import os
import unittest
from pathlib import Path

from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.levels.level import Level


class LevelTest(unittest.TestCase):
    player = PlayerCharacter(0, 0)
    cwd = os.path.realpath(__file__)
    path = Path(cwd)
    levels_dir = str(path.parent.absolute()) + os.sep + 'resources' + os.sep
    level_1 = Level(levels_dir + 'level_1.lvl', player)

    def test_loading(self):
        level_1 = Level(LevelTest.levels_dir + 'level_1.lvl', LevelTest.player)
        self.assertEqual(level_1.w, 4)
        self.assertEqual(level_1.h, 4)
        self.assertEqual(len(level_1.static_entities), 4)
        for st_ent_row in level_1.static_entities:
            self.assertEqual(len(st_ent_row), 4)
        self.assertEqual(len(level_1.acting_entities), 1)
        self.assertFalse(level_1.is_finished)
        self.assertEqual(level_1.finish_coord, (2, 2))
        self.assertEqual((LevelTest.player.x, LevelTest.player.y), (1, 1))

    def test_finish(self):
        LevelTest.player.x = 2
        LevelTest.player.y = 2

        self.assertFalse(LevelTest.level_1.is_finished)
        LevelTest.level_1.process_input(None)
        self.assertTrue(LevelTest.level_1.is_finished)

        LevelTest.player.x = 1
        LevelTest.player.y = 1
        LevelTest.level_1.is_finished = False

    def test_render(self):
        text, colors = LevelTest.level_1.render()
        self.assertEqual(text,
                         [[[['#', '#', '#', '#'], ['#', '@', ' ', '#'], ['#', ' ', 'X', '#'], ['#', '#', '#', '#']]],
                          [[str(LevelTest.level_1.player.stats)]]])


if __name__ == '__main__':
    unittest.main()
