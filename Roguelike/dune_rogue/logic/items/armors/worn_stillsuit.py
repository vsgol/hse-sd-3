from dune_rogue.logic.items.armors.armor import Armor
from dune_rogue.logic.stats import Stats


class WornStillsuit(Armor):
    """Worn stillsuit armor"""
    def __init__(self):
        super().__init__(weight=5, usable=False,
                         stats=Stats(0, 1, 0, 0), name='Worn stilsuit',
                         description='This stillsuit is not in the best condition but it still can help to survive in '
                                     'the desert',
                         )