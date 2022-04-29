from abc import ABC
from collections import deque


class Behavior(ABC):
    """NPC behavior basic class"""
    def __init__(self, previous=None):
        """
        :param previous: previous behavior
        """
        self.previous = previous

    def move(self, entity, mediator):
        """ Make decision
        :argument entity: game entity with this behavior
        :argument mediator: level mediator
        """
        raise NotImplementedError('move method is not implemented')

    def new_behavior(self, entity):
        """ Change behavior based on entity state
        :argument entity: entity to process
        :return: new behavior
        """
        return self

    @staticmethod
    def move_to_cell(entity, mediator, x_new, y_new):
        """ Move entity to new position or attack player at this position
        :argument entity: game entity which moves
        :argument mediator: level mediator
        :argument x_new: target x coordinate
        :argument y_new: target y coordinate
        """
        target = mediator.get_entity_at(x_new, y_new)

        entity.intersect(target)

        if not target.is_player:
            entity.x = x_new
            entity.y = y_new


def build_priority(w, h, x_player, y_player, x_entity, y_entity, mediator):
    """ Assigns priority to all positions where player is the best target and value decreases exponentially
    with distance increase
    :argument w: level width
    :argument h: level height
    :argument x_player: player x coordinate
    :argument y_player: player y coordinate
    :argument x_entity: entity x coordinate
    :argument y_entity: entity y coordinate
    :argument mediator: level mediator
    """
    priority = [[-2.0] * w for _ in range(h)]
    visited = [[False] * w for _ in range(h)]
    priority[y_player][x_player] = 1.0
    priority[y_entity][x_entity] = -1.0
    visited[y_player][x_player] = True
    discount = 0.99
    reached_entity = False

    static, acting = mediator.get_all_entities()
    for row in static:
        for ent in row:
            if ent.is_solid:
                visited[ent.y][ent.x] = True

    queue = deque()
    queue.append((x_player, y_player))
    while len(queue) > 0:
        x, y = queue.popleft()

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x_new = x + dx
            y_new = y + dy
            if x_new >= w or x_new < 0 or y_new >= h or y_new < 0 or visited[y_new][x_new]:
                continue
            priority[y_new][x_new] = priority[y][x] * discount
            visited[y][x] = True
            if y_new == y_entity and x_new == x_entity:
                reached_entity = True
            if not reached_entity:
                queue.append((x_new, y_new))

    return priority
