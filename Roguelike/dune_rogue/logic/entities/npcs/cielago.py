from dune_rogue.logic.ai.aggressive import AggressiveBehavior
from dune_rogue.logic.entities.npcs.npc import NPC
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class Cielago(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('c', Color(131, 67, 51)), AggressiveBehavior())
