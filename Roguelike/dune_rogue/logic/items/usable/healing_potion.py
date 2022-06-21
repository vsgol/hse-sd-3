from dune_rogue.logic.items.usable.usable import Usable
from dune_rogue.logic.stats import Stats


class HealingPotion(Usable):
    """Healing potion item"""
    def __init__(self):
        super().__init__(0.5, Stats(5, 0, 0, 0), "Healing potion", "Restores some health")

