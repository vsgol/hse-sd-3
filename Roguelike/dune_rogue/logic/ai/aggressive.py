import random
from collections import deque

from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.ai.random import RandomBehavior
from dune_rogue.logic.coordinate import Coordinate


class AggressiveBehavior(Behavior):
    """Entity seeks for player to attack if player near enough"""
    def __init__(self, radius=5):
        """
        :param radius: radius in which entity will chase player
        """
        super().__init__()
        self.radius_sq = radius ** 2

    @staticmethod
    def build_priority(w, h, player_coord, entity_coord, mediator):
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

    def within_perception(self, player_coord, entity_coord):
        diff = player_coord - entity_coord
        return diff.x ** 2 + diff.y ** 2 < self.radius_sq + 0.5

    def move(self, entity, mediator):
        player_coord = mediator.level.player.coord
        entity_coord = entity.coord
        w, h = mediator.get_level_shape()

        if not self.within_perception(player_coord, entity_coord):
            RandomBehavior().move(entity, mediator)
            return

        priority = self.build_priority(w, h, player_coord, entity_coord, mediator)
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


