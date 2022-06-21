from dune_rogue.logic.ai.aggressive import AggressiveBehavior
from dune_rogue.logic.ai.states import NormalState
from dune_rogue.logic.entities.npcs.npc import Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class Cymek(Enemy):
    """Cymek aggressive enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('C', Color(196, 202, 206)), AggressiveBehavior(NormalState()), 16,
                         stats=CharacterStats(6, 2, 2, 6, 0.2))
