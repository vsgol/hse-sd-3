from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.entities.npcs.npc import NPC, Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class KangarooMouse(Enemy):
    """Kangaroo mouse coward enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('m', Color(166, 145, 80)), CowardBehavior(), 2,
                         stats=CharacterStats(4, 0, 1, 4))
