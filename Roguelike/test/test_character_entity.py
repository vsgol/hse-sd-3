import unittest

from dune_rogue.logic.entities.player_character import PlayerCharacter


class CharacterTest(unittest.TestCase):
    def test_damage(self):
        player = PlayerCharacter(0, 0)

        player.make_damage(player.stats.defence + 1)
        self.assertEqual(player.stats.hp, player.stats.max_hp - 1)
        player.make_damage(player.stats.defence + 2)
        self.assertEqual(player.stats.hp, player.stats.max_hp - 3)


if __name__ == '__main__':
    unittest.main()
