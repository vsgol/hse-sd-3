import random

from dune_rogue.logic.ai.behavior import Behavior


class RandomBehavior(Behavior):
    """Move entity to the random available position"""
    def __init__(self):
        super().__init__()

    def move(self, entity, mediator):
        x_entity = entity.x
        y_entity = entity.y
        w, h = mediator.get_level_shape()

        available = [(x_entity, y_entity)]
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y, = x_entity + dx, y_entity + dy
            if w > x >= 0 and h > y >= 0 and not mediator.get_entity_at(x, y).is_solid:
                available.append((x_entity + dx, y_entity + dy))
        new_x, new_y = random.choice(available)

        self.move_to_cell(entity, mediator, new_x, new_y)
