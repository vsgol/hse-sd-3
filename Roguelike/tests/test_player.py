import random
import unittest
from copy import deepcopy

from dune_rogue.logic.ai.status_effects.confused import Confused
from dune_rogue.logic.entities.npcs.npc import Enemy, NPC
from dune_rogue.logic.entities.player_character import PlayerCharacter, CONFUSE_CHANCE
from dune_rogue.logic.items.armors.armor import Armor
from dune_rogue.logic.items.weapons.weapon import Weapon
from dune_rogue.logic.stats import CharacterStats, Stats, PlayerStats


class PlayerTest(unittest.TestCase):
    def test_intersect(self):
        NPC_ATK = 10
        NPC_HP = 10

        class DummyEnemy(Enemy):
            def __init__(self):
                super().__init__(0, 0, None, None, 3,
                                 stats=CharacterStats(NPC_HP, 0, NPC_ATK, NPC_HP))

        class DummyFriendly(NPC):
            def __init__(self):
                super().__init__(0, 0, None, None,
                                 stats=CharacterStats(NPC_HP, 0, NPC_ATK, NPC_HP), is_friendly=True)
        enemy = DummyEnemy()
        friend = DummyFriendly()
        player = PlayerCharacter(0, 0)
        player.stats.defence = 0

        player.intersect(friend)
        friend.intersect(player)
        self.assertEqual(player.stats.hp, player.stats.max_hp)
        self.assertEqual(friend.stats.hp, friend.stats.max_hp)

        player.intersect(enemy)
        enemy.intersect(player)
        self.assertEqual(player.stats.hp, player.stats.max_hp - NPC_ATK)
        self.assertEqual(enemy.stats.hp, enemy.stats.max_hp - player.stats.attack)

    def test_equip(self):
        ITEM_STATS = Stats(1, 2, 3, 4)
        ITEM_STATS_2 = Stats(-1, -2, -3, -4)
        PLAYER_STATS = PlayerStats(5, 6, 7, 8)

        class DummyWeapon(Weapon):
            def __init__(self):
                super().__init__(weight=0, usable=False,
                                 stats=ITEM_STATS, name=None,
                                 description=None,
                                 )

        class DummyWeapon2(Weapon):
            def __init__(self):
                super().__init__(weight=0, usable=False,
                                 stats=ITEM_STATS_2, name=None,
                                 description=None,
                                 )

        class DummyArmor(Armor):
            def __init__(self):
                super().__init__(weight=0, usable=False,
                                 stats=ITEM_STATS, name=None,
                                 description=None,
                                 )

        class DummyArmor2(Armor):
            def __init__(self):
                super().__init__(weight=0, usable=False,
                                 stats=ITEM_STATS_2, name=None,
                                 description=None,
                                 )

        player = PlayerCharacter(0, 0)
        player.stats = deepcopy(PLAYER_STATS)

        w1 = DummyWeapon()
        w2 = DummyWeapon2()
        a1 = DummyArmor()
        a2 = DummyArmor2()

        player.equip_item(w1)
        self.assertEqual(player.stats, PLAYER_STATS + ITEM_STATS)
        self.assertTrue(w1.is_equipped)
        self.assertIs(player.weapon, w1)
        player.equip_item(w2)
        self.assertEqual(player.stats, PLAYER_STATS + ITEM_STATS_2)
        self.assertFalse(w1.is_equipped)
        self.assertTrue(w2.is_equipped)
        self.assertIs(player.weapon, w2)

        player.equip_item(a1)
        self.assertEqual(player.stats, PLAYER_STATS + ITEM_STATS_2 + ITEM_STATS)
        self.assertTrue(a1.is_equipped)
        self.assertIs(player.armor, a1)
        player.equip_item(a2)
        self.assertEqual(player.stats, PLAYER_STATS + ITEM_STATS_2 + ITEM_STATS_2)
        self.assertFalse(a1.is_equipped)
        self.assertTrue(a2.is_equipped)
        self.assertIs(player.armor, a2)

        player.unequip_item(w2)
        self.assertEqual(player.stats, PLAYER_STATS + ITEM_STATS_2)
        self.assertFalse(w2.is_equipped)
        self.assertIs(player.weapon, None)
        player.unequip_item(a2)
        self.assertEqual(player.stats, PLAYER_STATS)
        self.assertFalse(a2.is_equipped)
        self.assertIs(player.weapon, None)

    def test_confusion(self):
        class DummyEnemy(Enemy):
            def __init__(self):
                super().__init__(0, 0, None, None, 3,
                                 stats=CharacterStats())

        player = PlayerCharacter(0, 0)
        enemy = DummyEnemy()

        random.seed(0)
        for _ in range(int(1 / CONFUSE_CHANCE * 10)):
            player.intersect(enemy)
        self.assertTrue(isinstance(enemy.behavior, Confused))


if __name__ == '__main__':
    unittest.main()
