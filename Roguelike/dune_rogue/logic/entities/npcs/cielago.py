from dune_rogue.logic.ai.aggressive import AggressiveBehavior
from dune_rogue.logic.entities.npcs.npc import Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class Cielago(Enemy):
    """Cielago aggressive enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('c', Color(131, 67, 51)), AggressiveBehavior(), 3,
                         stats=CharacterStats(4, 1, 1, 4, 0.2))
