import random
from collections import deque

from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.ai.random import RandomBehavior


class AggressiveBehavior(Behavior):
    def __init__(self, radius=25):
        super().__init__()
        self.radius = radius

    @staticmethod
    def build_priority(w, h, x_player, y_player, x_entity, y_entity, mediator):
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

    def move(self, entity, mediator):
        x_player = mediator.level.player.x
        y_player = mediator.level.player.y
        x_entity = entity.x
        y_entity = entity.y
        w, h = mediator.get_level_shape()

        if (x_player - x_entity) ** 2 + (y_player - y_entity) ** 2 >= self.radius + 0.5:
            RandomBehavior().move(entity, mediator)
            return

        priority = self.build_priority(w, h, x_player, y_player, x_entity, y_entity, mediator)
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


if __name__ == '__main__':
    x_player = 0
    y_player = 0
    class DummyEnt:
        is_solid = False
    class DummyMed:
        def get_entity_at(self, x, y):
            e = DummyEnt()
            if x == x_player and y == y_player:
                e.is_solid = True
            return e

    p = AggressiveBehavior().build_priority(5, 5, x_player, y_player, 1, 2, DummyMed())
    for r in p:
        print(r)


