import unittest

from dune_rogue.logic.inventory import Inventory
from dune_rogue.logic.items.item import InventoryItem
from dune_rogue.logic.stats import Stats


class InventoryTest(unittest.TestCase):
    stats = Stats(1, 2, 3, 4)
    item_0 = InventoryItem(stats=stats, weight=0)
    item_1 = InventoryItem(stats=stats, weight=1)
    item_2 = InventoryItem(stats=stats, weight=2)
    item_4 = InventoryItem(stats=stats, weight=4)

    def test_init(self):
        inventory = Inventory(capacity=7)
        self.assertEqual(inventory.capacity, 7)
        self.assertEqual(inventory.weight, 0)
        self.assertEqual(len(inventory.items), 0)

        inventory = Inventory(capacity=7, items=[InventoryTest.item_1, InventoryTest.item_2, InventoryTest.item_4])
        self.assertEqual(inventory.capacity, 7)
        self.assertEqual(inventory.weight, 7)
        self.assertEqual(len(inventory.items), 3)

        with self.assertRaises(RuntimeError):
            Inventory(capacity=7, items=[InventoryTest.item_4, InventoryTest.item_4])

    def test_can_take(self):
        inventory = Inventory(capacity=7)
        for i in range(8):
            self.assertTrue(inventory.can_take(i))

        self.assertFalse(inventory.can_take(8))

    def test_add(self):
        inventory = Inventory(capacity=7)

        self.assertEqual(inventory.weight, 0)
        self.assertTrue(inventory.can_take(7))
        inventory.add_item(InventoryTest.item_4)
        self.assertFalse(inventory.can_take(4))
        self.assertEqual(inventory.weight, 4)
        with self.assertRaises(RuntimeError):
            inventory.add_item(InventoryTest.item_4)

        self.assertEqual(inventory.weight, 4)
        self.assertTrue(inventory.can_take(3))
        inventory.add_item(InventoryTest.item_2)
        self.assertEqual(inventory.weight, 6)
        self.assertFalse(inventory.can_take(2))
        with self.assertRaises(RuntimeError):
            inventory.add_item(InventoryTest.item_2)

        self.assertEqual(inventory.weight, 6)
        self.assertTrue(inventory.can_take(1))
        inventory.add_item(InventoryTest.item_1)
        self.assertEqual(inventory.weight, 7)
        self.assertFalse(inventory.can_take(1))
        with self.assertRaises(RuntimeError):
            inventory.add_item(InventoryTest.item_1)

        self.assertEqual(inventory.weight, 7)
        self.assertTrue(inventory.can_take(0))
        inventory.add_item(InventoryTest.item_0)
        self.assertTrue(inventory.can_take(0))
        inventory.add_item(InventoryTest.item_0)
        self.assertEqual(inventory.weight, 7)

    def test_remove(self):
        inventory = Inventory(capacity=7, items=[InventoryTest.item_1, InventoryTest.item_2, InventoryTest.item_4])

        self.assertEqual(len(inventory.items), 3)
        self.assertEqual(inventory.weight, 7)
        self.assertFalse(inventory.can_take(1))
        inventory.remove_item(0)
        self.assertEqual(inventory.weight, 6)
        self.assertTrue(inventory.can_take(1))
        self.assertFalse(inventory.can_take(2))
        self.assertEqual(len(inventory.items), 2)

        inventory.remove_item(0)
        self.assertEqual(len(inventory.items), 1)
        self.assertEqual(inventory.weight, 4)
        self.assertTrue(inventory.can_take(3))
        self.assertFalse(inventory.can_take(4))

        inventory.remove_item(0)
        self.assertEqual(len(inventory.items), 0)
        self.assertEqual(inventory.weight, 0)
        self.assertTrue(inventory.can_take(7))
        self.assertFalse(inventory.can_take(8))

        inventory = Inventory(capacity=7, items=[InventoryTest.item_1, InventoryTest.item_2, InventoryTest.item_4])

        inventory.remove_item(2)
        self.assertEqual(len(inventory.items), 2)
        self.assertEqual(inventory.weight, 3)
        self.assertTrue(inventory.can_take(4))
        self.assertFalse(inventory.can_take(5))

        inventory.remove_item(1)
        self.assertEqual(len(inventory.items), 1)
        self.assertEqual(inventory.weight, 1)
        self.assertTrue(inventory.can_take(2))
        self.assertFalse(inventory.can_take(7))

        inventory.capacity = 0
        inventory.weight = 10
        with self.assertRaises(RuntimeError):
            inventory.remove_item(0)
        self.assertEqual(inventory.weight, 10)


if __name__ == '__main__':
    unittest.main()
