import random
from collections import deque

from dune_rogue.logic.ai.aggressive import AggressiveBehavior
from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.ai.random import RandomBehavior
from dune_rogue.logic.coordinate import Coordinate


class CowardBehavior(AggressiveBehavior):
    """Entity escapes for player when player near enough"""
    def __init__(self, radius=5):
        super().__init__(radius)

    def move(self, entity, mediator):
        player_coord = mediator.level.player.coord
        entity_coord = entity.coord
        w, h = mediator.get_level_shape()

        if not self.within_perception(player_coord, entity_coord):
            RandomBehavior().move(entity, mediator)
            return

        neg_priority = self.build_priority(w, h, player_coord, entity_coord, mediator)
        neg_priority[entity_coord.y][entity_coord.x] *= -1

        static, acting = mediator.get_all_entities()
        for row in static:
            for ent in row:
                if ent.is_solid:
                    neg_priority[ent.y][ent.x] *= -1

        max_p = -1
        candidates = []

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coord = entity_coord + Coordinate(dx, dy)
            if not mediator.inside_level(coord):
                continue
            p = -neg_priority[coord.y][coord.x]
            if not (max_p <= p and self.acceptable_position(coord, entity_coord)):
                continue
            if max_p == p:
                candidates.append(coord)
            else:
                max_p = p
                candidates = [coord]

        new = random.choice(candidates)
        if not (new == player_coord) and mediator.get_entity_at(new).is_solid:
            new = entity_coord
        self.move_to_cell(entity, mediator, new)
