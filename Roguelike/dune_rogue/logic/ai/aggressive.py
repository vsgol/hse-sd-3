import random
from collections import deque

from dune_rogue.logic.ai.behavior import Behavior, build_priority
from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.ai.random import RandomBehavior, random_position
from dune_rogue.logic.coordinate import Coordinate


class AggressiveBehavior(Behavior):
    """Entity seeks for player to attack if player near enough"""
    def __init__(self, initial_state, radius=5):
        """
        :param radius: radius in which entity will chase player
        """
        super().__init__(initial_state)
        self.radius_sq = radius ** 2

    def act(self, entity, mediator):
        player_coord = mediator.level.player.coord
        entity_coord = entity.coord
        w, h = mediator.get_level_shape()

        if not self.within_perception(player_coord, entity_coord):
            new = random_position(entity, mediator)
            self.move_to_cell(entity, mediator, new)
            return

        priority = build_priority(w, h, player_coord, entity_coord, mediator)
        max_p = -1
        candidates = []
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coord = entity_coord + Coordinate(dx, dy)
            if not mediator.inside_level(coord):
                continue
            p = priority[coord.y][coord.x]
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

