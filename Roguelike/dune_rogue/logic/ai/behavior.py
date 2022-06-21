import sys
from abc import ABC
from collections import deque

from dune_rogue.logic.coordinate import Coordinate


class Behavior(ABC):
    """NPC behavior basic class"""

    def __init__(self, initial_state):
        """
        :param initial_state: initial state
        """
        self.radius_sq = float('inf')
        self.current_state = initial_state

    def move(self, entity, mediator):
        """ Make decision based on the current state
        :argument entity: game entity with this behavior
        :argument mediator: level mediator
        """
        self.current_state.update_state(entity)
        self.current_state.move(entity, mediator)

    def act(self, entity, mediator):
        """ Make default decision
        :argument entity: game entity with this behavior
        :argument mediator: level mediator
        """
        assert False  # move is not implemented

    @staticmethod
    def move_to_cell(entity, mediator, new_coord):
        """ Move entity to new position or attack player at this position
        :argument entity: game entity which moves
        :argument mediator: level mediator
        :argument new_coord: target coordinate
        """
        target = mediator.get_entity_at(new_coord)

        entity.intersect(target)

        if not target.is_player:
            entity.coord = new_coord

    @staticmethod
    def acceptable_position(new_pos, entity_pos):
        return new_pos.x == entity_pos.x and abs(new_pos.y - entity_pos.y) <= 1 or \
               new_pos.y == entity_pos.y and abs(new_pos.x - entity_pos.x) <= 1

    def within_perception(self, player_coord, entity_coord):
        diff = player_coord - entity_coord
        return diff.x ** 2 + diff.y ** 2 < self.radius_sq + 0.5


def build_priority(w, h, player_coord, entity_coord, mediator):
    """ Assigns priority to all positions where player is the best target and value decreases exponentially
    with distance increase
    :argument w: level width
    :argument h: level height
    :argument player_coord: player coordinate
    :argument entity_coord: entity coordinate
    :argument mediator: level mediator
    """
    priority = [[-2.0] * w for _ in range(h)]
    visited = [[False] * w for _ in range(h)]
    priority[player_coord.y][player_coord.x] = 1.0
    priority[entity_coord.y][entity_coord.x] = -1.0
    visited[player_coord.y][player_coord.x] = True
    discount = 0.99
    reached_entity = False

    static, acting = mediator.get_all_entities()
    for row in static:
        for ent in row:
            if ent.is_solid:
                visited[ent.y][ent.x] = True

    queue = deque()
    queue.append(player_coord)

    while len(queue) > 0:
        coord = queue.popleft()

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new = coord + Coordinate(dx, dy)
            if not mediator.inside_level(new) or visited[new.y][new.x]:
                continue
            priority[new.y][new.x] = priority[coord.y][coord.x] * discount
            visited[coord.y][coord.x] = True
            if new == entity_coord:
                reached_entity = True
            if not reached_entity:
                queue.append(new)

    return priority
