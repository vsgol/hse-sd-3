import random

from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.coordinate import Coordinate


class RandomBehavior(Behavior):
    """Move entity to the random available position"""
    def __init__(self):
        super().__init__()

    def move(self, entity, mediator):
        entity_coord = entity.coord

        available = [entity_coord]
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coord = entity_coord + Coordinate(dx, dy)
            if mediator.inside_level(coord) and not mediator.get_entity_at(coord).is_solid:
                available.append(coord)
        new = random.choice(available)

        self.move_to_cell(entity, mediator, new)
