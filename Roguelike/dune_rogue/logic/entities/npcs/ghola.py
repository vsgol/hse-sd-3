from copy import deepcopy

from dune_rogue.logic.ai.passive import PassiveBehavior
from dune_rogue.logic.coordinate import Coordinate
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
        return Coordinate(x, y)

    @staticmethod
    def get_neighbors_count(e_coord, mediator):
        cnt = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]:
            coord = e_coord + Coordinate(dx, dy)
            coord = Ghola.scale_coords(coord.x, coord.y, mediator)

            ent_at = mediator.get_entity_at(coord)
            if ent_at is not None and isinstance(ent_at, Ghola):
                cnt += 1
        return cnt

    def clone(self, mediator):
        e_coord = self.coord

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]:
            coord = e_coord + Coordinate(dx, dy)

            coord = Ghola.scale_coords(coord.x, coord.y, mediator)

            ent_at = mediator.get_entity_at(coord)
            if ent_at is None or ent_at.is_solid or mediator.new_coords[coord.y][coord.x]:
                continue

            nbs = self.get_neighbors_count(coord, mediator)
            if nbs == 3:
                clone = deepcopy(self)
                clone.coord = coord
                mediator.add_entity(clone)

    def update(self, mediator):
        self.behavior.move(self, mediator)
        self.clone(mediator)
        nbs = self.get_neighbors_count(self.coord, mediator)
        if not (2 <= nbs <= 3):
            self.exp = 0
            self.is_alive = False
            self.stats.hp = 0

