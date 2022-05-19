from abc import ABC


class Behavior(ABC):
    """NPC behavior basic class"""
    def __init__(self):
        pass

    def move(self, entity, mediator):
        """ Make decision
        :argument entity: game entity with this behavior
        :argument mediator: level mediator
        """
        raise NotImplementedError('move method is not implemented')

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
