from copy import deepcopy

from dune_rogue.logic.ai.passive import PassiveBehavior
from dune_rogue.logic.entities.npcs.npc import Replicating
from dune_rogue.logic.stats import CharacterStats
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class Ghola(Replicating):
    """Ghola passive enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, Glyph('G', Color(229, 194, 152)), PassiveBehavior(), 3, 1,
                         stats=CharacterStats(2, 0, 1, 2))

    @staticmethod
    def scale_coords(x, y, mediator):
        if y == mediator.level.h - 1:
            y = 1
        elif y == 0:
            y = mediator.level.h - 2
        if x == mediator.level.w - 1:
            x = 1
        elif x == 0:
            x = mediator.level.w - 2
        return x, y

    @staticmethod
    def get_neighbors_count(ex, ey, mediator):
        cnt = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]:
            x = ex + dx
            y = ey + dy
            x, y = Ghola.scale_coords(x, y, mediator)

            ent_at = mediator.get_entity_at(x, y)
            if ent_at is not None and isinstance(ent_at, Ghola):
                cnt += 1
        return cnt

    def clone(self, mediator):
        ex = self.x
        ey = self.y

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]:
            x = ex + dx
            y = ey + dy
            x, y = Ghola.scale_coords(x, y, mediator)

            ent_at = mediator.get_entity_at(x, y)
            if ent_at is None or ent_at.is_solid or mediator.new_coords[y][x]:
                continue

            nbs = self.get_neighbors_count(x, y, mediator)
            if nbs == 3:
                clone = deepcopy(self)
                clone.x = x
                clone.y = y
                mediator.add_entity(clone)

    def update(self, mediator):
        self.behavior.move(self, mediator)
        self.clone(mediator)
        nbs = self.get_neighbors_count(self.x, self.y, mediator)
        if not (2 <= nbs <= 3):
            self.exp = 0
            self.is_alive = False
            self.stats.hp = 0

