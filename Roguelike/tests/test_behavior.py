import os
import unittest
from pathlib import Path

from dune_rogue.logic.actions import Action
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.levels.level import Level
from dune_rogue.logic.levels.mediator import LevelMediator


class BehaviorTest(unittest.TestCase):
    player = PlayerCharacter(0, 0)
    cwd = os.path.realpath(__file__)
    path = Path(cwd)
    levels_dir = str(path.parent.absolute()) + os.sep + 'resources' + os.sep

    def test_aggressive(self):
        corridor = Level(self.levels_dir + 'corridor.lvl', self.player)
        mediator = LevelMediator(corridor)
        aggressive = corridor.acting_entities[2]

        priority = aggressive.behavior.build_priority(corridor.w, corridor.h,
                                                      self.player.coord,
                                                      aggressive.coord, mediator)

        target = [[-2.0] * corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(corridor.w - 2)] + [-2.0],
                  [-2.0] * corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        aggressive_prev = (aggressive.x, aggressive.y)

        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((aggressive.x, aggressive.y), (aggressive_prev[0] - 1, aggressive_prev[1]))

        priority = aggressive.behavior.build_priority(corridor.w, corridor.h,
                                                      self.player.coord,
                                                      aggressive.coord, mediator)

        target = [[-2.0] * corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(corridor.w - 3)] + [-2.0, -2.0],
                  [-2.0] * corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        aggressive_prev = (aggressive.x, aggressive.y)

        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((aggressive.x, aggressive.y), (aggressive_prev[0], aggressive_prev[1]))

    def test_coward(self):
        corridor = Level(self.levels_dir + 'corridor.lvl', self.player)
        mediator = LevelMediator(corridor)
        coward = corridor.acting_entities[1]

        priority = coward.behavior.build_priority(corridor.w, corridor.h,
                                                  self.player.coord,
                                                  coward.coord, mediator)
        target = [[-2.0] * corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(2)] + [-2.0] * (corridor.w - 3),
                  [-2.0] * corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        coward_prev = (coward.x, coward.y)
        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((coward.x, coward.y), (coward_prev[0] + 1, coward_prev[1]))

        priority = coward.behavior.build_priority(corridor.w, corridor.h,
                                                  self.player.coord,
                                                  coward.coord, mediator)
        target = [[-2.0] * corridor.w,
                  [-2.0] + [round(0.99 ** i, 2) for i in range(3)] + [-2.0] * (corridor.w - 4),
                  [-2.0] * corridor.w]
        priority = list(map(lambda x: list(map(lambda e: round(e, 2), x)), priority))
        self.assertListEqual(priority, target)

        coward_prev = (coward.x, coward.y)

        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((coward.x, coward.y), coward_prev)

    def test_passive(self):
        corridor = Level(self.levels_dir + 'corridor.lvl', self.player)
        passive = corridor.acting_entities[3]

        passive_prev = (passive.x, passive.y)

        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((passive.x, passive.y), passive_prev)

        passive_prev = (passive.x, passive.y)

        corridor.process_input(Action.MOVE_DOWN)
        self.assertEqual((passive.x, passive.y), passive_prev)


if __name__ == '__main__':
    unittest.main()
