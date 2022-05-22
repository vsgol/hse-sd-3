from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.ai.states import NormalState
from dune_rogue.logic.entities.npcs.npc import NPC, Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class Valetbot(Enemy):
    """Valetbot coward enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('V', Color(161, 157, 148)), CowardBehavior(NormalState()), 10,
                         stats=CharacterStats(6, 1, 2, 6))
