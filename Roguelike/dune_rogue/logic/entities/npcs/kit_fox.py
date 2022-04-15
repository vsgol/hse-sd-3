from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.ai.passive import PassiveBehavior
from dune_rogue.logic.entities.npcs.npc import NPC, Enemy
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class KitFox(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('f', Color(183, 88, 0)), PassiveBehavior(), 3,
                         stats=CharacterStats(6, 1, 1, 6))
