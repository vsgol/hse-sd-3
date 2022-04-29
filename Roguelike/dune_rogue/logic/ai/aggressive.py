import random
from collections import deque

from dune_rogue.logic.ai.behavior import Behavior, build_priority
from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.ai.random import RandomBehavior


class AggressiveBehavior(Behavior):
    """Entity seeks for player to attack if player near enough"""
    def __init__(self, radius=25, previous=None):
        """
        :param radius: radius in which entity will chase player
        """
        super().__init__(previous)
        self.radius = radius

    def new_behavior(self, entity):
        if 3 * entity.stats.hp <= entity.stats.max_hp:
            return CowardBehavior(previous=self)
        return self

    def move(self, entity, mediator):
        x_player = mediator.level.player.x
        y_player = mediator.level.player.y
        x_entity = entity.x
        y_entity = entity.y
        w, h = mediator.get_level_shape()

        if (x_player - x_entity) ** 2 + (y_player - y_entity) ** 2 >= self.radius + 0.5:
            RandomBehavior().move(entity, mediator)
            return

        priority = build_priority(w, h, x_player, y_player, x_entity, y_entity, mediator)
        max_p = -1
        candidates = []
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y, = x_entity + dx, y_entity + dy
            if w > x >= 0 and h > y >= 0:
                p = priority[y][x]
                if max_p <= p and (x == x_entity and abs(y - y_entity) <= 1 or y == y_entity and abs(x - x_entity) <= 1):
                    if max_p == p:
                        candidates.append((x, y))
                    else:
                        max_p = p
                        candidates = [(x, y)]

        new_x, new_y = random.choice(candidates)
        if (new_x != x_player or new_y != y_player) and mediator.get_entity_at(new_x, new_y).is_solid:
            new_x, new_y = x_entity, y_entity
        self.move_to_cell(entity, mediator, new_x, new_y)
