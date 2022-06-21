from abc import ABC

from dune_rogue.logic.items.item import InventoryItem


class Armor(InventoryItem, ABC):
    """Armor base class"""
    def __init__(self, weight=0, usable=False, stats=None, name="Default name",
                 description='Default description', is_equipped=False):
        super().__init__(weight, usable, True, stats, name,
                         description, is_equipped, item_type='Armor')
