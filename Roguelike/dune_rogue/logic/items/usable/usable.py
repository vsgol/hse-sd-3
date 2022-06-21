from abc import ABC

from dune_rogue.logic.items.item import InventoryItem


class Usable(InventoryItem, ABC):
    """Usable item base class"""
    def __init__(self, weight=0, stats=None, name="Default name",
                 description='Default description'):
        super().__init__(weight, True, False, stats, name,
                         description, False, item_type='Usable')
