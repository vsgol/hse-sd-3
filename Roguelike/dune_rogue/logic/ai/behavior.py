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
