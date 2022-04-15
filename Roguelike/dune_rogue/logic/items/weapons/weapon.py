from abc import ABC

from dune_rogue.logic.items.item import InventoryItem


class Weapon(InventoryItem, ABC):
    def __init__(self, weight=0, usable=False, can_be_equipped=False, stats=None, name="Default name",
                 description='Default description', is_equipped=False):
        super().__init__(weight, usable, can_be_equipped, stats, name,
                 description, is_equipped)