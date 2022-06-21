import unittest

from dune_rogue.logic.items.item import InventoryItem
from dune_rogue.logic.stats import Stats


class ItemsTest(unittest.TestCase):
    stats = Stats(1, 2, 3, 4)

    def test_equipable_item(self):
        item = InventoryItem(stats=ItemsTest.stats, can_be_equipped=True)

        item_stats = item.get_bonuses()

        self.assertEqual(ItemsTest.stats.hp, item_stats.hp)
        self.assertEqual(ItemsTest.stats.defence, item_stats.defence)
        self.assertEqual(ItemsTest.stats.attack, item_stats.attack)
        self.assertEqual(ItemsTest.stats.max_hp, item_stats.max_hp)

        self.assertFalse(item.is_equipped)
        item.equip()
        self.assertTrue(item.is_equipped)
        with self.assertRaises(RuntimeError):
            item.equip()
        self.assertTrue(item.is_equipped)
        item.unequip()
        self.assertFalse(item.is_equipped)
        with self.assertRaises(RuntimeError):
            item.unequip()
        self.assertFalse(item.is_equipped)

    def test_unequipable_item(self):
        item = InventoryItem(stats=ItemsTest.stats, can_be_equipped=False)

        item_stats = item.get_bonuses()

        self.assertEqual(ItemsTest.stats.hp, item_stats.hp)
        self.assertEqual(ItemsTest.stats.defence, item_stats.defence)
        self.assertEqual(ItemsTest.stats.attack, item_stats.attack)
        self.assertEqual(ItemsTest.stats.max_hp, item_stats.max_hp)

        self.assertFalse(item.is_equipped)
        with self.assertRaises(RuntimeError):
            item.equip()
        self.assertFalse(item.is_equipped)
        with self.assertRaises(RuntimeError):
            item.unequip()
        self.assertFalse(item.is_equipped)

    def test_str(self):
        item = InventoryItem(stats=ItemsTest.stats)
        self.assertEqual(item.get_bonuses_str(), f'HP: +{item.stats.hp} DEF: +{item.stats.defence} '
                                                 f'ATK: +{item.stats.attack} MAX_HP: +{item.stats.max_hp}')
        neg_item = InventoryItem(stats=Stats(-1, -2, -3, -4))
        self.assertEqual(neg_item.get_bonuses_str(), f'HP: {neg_item.stats.hp} DEF: {neg_item.stats.defence} '
                                                     f'ATK: {neg_item.stats.attack} MAX_HP: {neg_item.stats.max_hp}')
        zeros_item = InventoryItem(stats=Stats(-1, 0, -3, 0))
        self.assertEqual(zeros_item.get_bonuses_str(), f'HP: {zeros_item.stats.hp} '
                                                     f'ATK: {zeros_item.stats.attack}')


if __name__ == '__main__':
    unittest.main()
