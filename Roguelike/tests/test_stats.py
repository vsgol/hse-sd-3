import unittest

from dune_rogue.logic.stats import Stats, CharacterStats, PlayerStats


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

    def test_character_stats(self):
        stats1 = Stats(StatsTest.HP1, StatsTest.DEF1, StatsTest.ATK1, StatsTest.MHP1)
        stats2 = CharacterStats(StatsTest.HP2, StatsTest.DEF2, StatsTest.ATK2, StatsTest.MHP2)

        stats2.add_stats(stats1)
        self.check_correct(stats2,
                           StatsTest.HP1 + StatsTest.HP2,
                           StatsTest.DEF1 + StatsTest.DEF2,
                           StatsTest.ATK1 + StatsTest.ATK2,
                           StatsTest.MHP1 + StatsTest.MHP2
                           )
        stats2.remove_stats(stats1)
        self.check_correct(stats2,
                           StatsTest.HP2,
                           StatsTest.DEF2,
                           StatsTest.ATK2,
                           StatsTest.MHP2
                           )
        stats2.remove_stats(stats1)
        self.check_correct(stats2,
                           StatsTest.HP2 - StatsTest.HP1,
                           StatsTest.DEF2 - StatsTest.DEF1,
                           StatsTest.ATK2 - StatsTest.ATK1,
                           StatsTest.MHP2 - StatsTest.MHP1)

    def test_player_stats(self):
        stats = PlayerStats(StatsTest.HP1, StatsTest.DEF1, StatsTest.ATK1, StatsTest.MHP1)
        stats.give_exp(1)
        self.assertEqual(stats.exp, 1)
        self.assertEqual(stats.level, 0)
        stats.give_exp(6)
        self.assertEqual(stats.exp, 7)
        self.assertEqual(stats.level, 0)
        stats.give_exp(1)
        self.assertEqual(stats.exp, 0)
        self.assertEqual(stats.level, 1)
        self.check_correct(stats,
                           StatsTest.HP1,
                           StatsTest.DEF1 + 1,
                           StatsTest.ATK1 + 1,
                           StatsTest.MHP1 + 1)
        stats.give_exp(17)
        self.assertEqual(stats.exp, 1)
        self.assertEqual(stats.level, 2)
        self.check_correct(stats,
                           StatsTest.HP1,
                           StatsTest.DEF1 + 2,
                           StatsTest.ATK1 + 2,
                           StatsTest.MHP1 + 2)


if __name__ == '__main__':
    unittest.main()
