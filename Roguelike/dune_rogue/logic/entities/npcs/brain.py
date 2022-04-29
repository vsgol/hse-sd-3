from dune_rogue.logic.ai.passive import PassiveBehavior
from dune_rogue.logic.entities.npcs.npc import Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class BrainInAJar(Enemy):
    """Brain in a jar passive enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('B', Color(0, 78, 56)), PassiveBehavior(), 10,
                         stats=CharacterStats(6, 2, 1, 6, 0.2))
