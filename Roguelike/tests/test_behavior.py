import os
import unittest
from pathlib import Path

from dune_rogue.logic.actions import Action
from dune_rogue.logic.ai.behavior import build_priority
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.levels.level import Level
from dune_rogue.logic.levels.mediator import LevelMediator


class BehaviorTest(unittest.TestCase):
    player = PlayerCharacter(0, 0)
    cwd = os.path.realpath(__file__)
    path = Path(cwd)
    levels_dir = str(path.parent.absolute()) + os.sep + 'resources' + os.sep
    corridor = Level(levels_dir + 'corridor.lvl', player)

    def test_corridor(self):
        mediator = LevelMediator(self.corridor)
        coward = self.corridor.acting_entities[1]
        aggressive = self.corridor.acting_entities[2]
        passive = self.corridor.acting_entities[3]

        priority = build_priority(self.corridor.w, self.corridor.h,
                                  self.player.x, self.player.y,
                                  aggressive.x, aggressive.y, mediator)

        target = [[-2.0] * self.corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(self.corridor.w - 2)] + [-2.0],
                  [-2.0] * self.corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        priority = build_priority(self.corridor.w, self.corridor.h,
                                  self.player.x, self.player.y,
                                  coward.x, coward.y, mediator)
        target = [[-2.0] * self.corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(2)] + [-2.0] * (self.corridor.w - 3),
                  [-2.0] * self.corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        coward_prev = (coward.x, coward.y)
        aggressive_prev = (aggressive.x, aggressive.y)
        passive_prev = (passive.x, passive.y)

        self.corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((coward.x, coward.y), (coward_prev[0] + 1, coward_prev[1]))
        self.assertEqual((aggressive.x, aggressive.y), (aggressive_prev[0] - 1, aggressive_prev[1]))
        self.assertEqual((passive.x, passive.y), passive_prev)

        priority = build_priority(self.corridor.w, self.corridor.h,
                                  self.player.x, self.player.y,
                                  aggressive.x, aggressive.y, mediator)

        target = [[-2.0] * self.corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(self.corridor.w - 3)] + [-2.0, -2.0],
                  [-2.0] * self.corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        priority = build_priority(self.corridor.w, self.corridor.h,
                                  self.player.x, self.player.y,
                                  coward.x, coward.y, mediator)
        target = [[-2.0] * self.corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(3)] + [-2.0] * (self.corridor.w - 4),
                  [-2.0] * self.corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        coward_prev = (coward.x, coward.y)
        aggressive_prev = (aggressive.x, aggressive.y)
        passive_prev = (passive.x, passive.y)

        self.corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((coward.x, coward.y), coward_prev)
        self.assertEqual((aggressive.x, aggressive.y), (aggressive_prev[0], aggressive_prev[1]))
        self.assertEqual((passive.x, passive.y), passive_prev)

        self.corridor = Level(self.levels_dir + 'corridor.lvl', self.player)


if __name__ == '__main__':
    unittest.main()
