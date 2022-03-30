import unittest

from dune_rogue.logic.stats import Stats


class StatsTest(unittest.TestCase):
    HP1 = 1
    DEF1 = 2
    ATK1 = 3
    MHP1 = 4
    HP2 = 5
    DEF2 = 6
    ATK2 = 7
    MHP2 = 8

    def check_correct(self, stats, hp, defence, attack, max_hp):
        self.assertEqual(stats.hp, hp)
        self.assertEqual(stats.defence, defence)
        self.assertEqual(stats.attack, attack)
        self.assertEqual(stats.max_hp, max_hp)

    def test_init(self):
        stats = Stats(StatsTest.HP1, StatsTest.DEF1, StatsTest.ATK1, StatsTest.MHP1)
        self.check_correct(stats, StatsTest.HP1, StatsTest.DEF1, StatsTest.ATK1, StatsTest.MHP1)

    def test_ops(self):
        stats1 = Stats(StatsTest.HP1, StatsTest.DEF1, StatsTest.ATK1, StatsTest.MHP1)
        stats2 = Stats(StatsTest.HP2, StatsTest.DEF2, StatsTest.ATK2, StatsTest.MHP2)
        stats_sum_1 = stats1 + stats2
        stats_sum_2 = stats2 + stats1
        stats_sub_1 = stats1 - stats2
        stats_sub_2 = stats2 - stats1

        self.check_correct(stats_sum_1,
                           StatsTest.HP1 + StatsTest.HP2,
                           StatsTest.DEF1 + StatsTest.DEF2,
                           StatsTest.ATK1 + StatsTest.ATK2,
                           StatsTest.MHP1 + StatsTest.MHP2)

        self.check_correct(stats_sum_2,
                           StatsTest.HP1 + StatsTest.HP2,
                           StatsTest.DEF1 + StatsTest.DEF2,
                           StatsTest.ATK1 + StatsTest.ATK2,
                           StatsTest.MHP1 + StatsTest.MHP2)

        self.check_correct(stats_sub_1,
                           StatsTest.HP1 - StatsTest.HP2,
                           StatsTest.DEF1 - StatsTest.DEF2,
                           StatsTest.ATK1 - StatsTest.ATK2,
                           StatsTest.MHP1 - StatsTest.MHP2)

        self.check_correct(stats_sub_2,
                           StatsTest.HP2 - StatsTest.HP1,
                           StatsTest.DEF2 - StatsTest.DEF1,
                           StatsTest.ATK2 - StatsTest.ATK1,
                           StatsTest.MHP2 - StatsTest.MHP1)


if __name__ == '__main__':
    unittest.main()
