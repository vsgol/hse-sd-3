import random

from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.coordinate import Coordinate


def random_position(entity, mediator):
    """ Get random postion for the entity
    :argument entity: game entity with this behavior
    :argument mediator: level mediator
    :returns: new position
    """
    entity_coord = entity.coord

    available = [entity_coord]
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        coord = entity_coord + Coordinate(dx, dy)
        if mediator.inside_level(coord) and not mediator.get_entity_at(coord).is_solid:
            available.append(coord)
    return random.choice(available)


class RandomBehavior(Behavior):
    """Move entity to the random available position"""

    def move(self, entity, mediator):
        new = random_position(entity, mediator)
        self.move_to_cell(entity, mediator, new)
