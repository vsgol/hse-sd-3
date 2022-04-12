from abc import ABC

from dune_rogue.logic.entities.player_character import PlayerCharacter


class Behavior(ABC):
    def __init__(self):
        pass

    def move(self, entity, mediator):
        raise NotImplementedError('move method is not implemented')

    def move_to_cell(self, entity, mediator, x_new, y_new):
        target = mediator.get_entity_at(x_new, y_new)

        entity.intersect(target)
        target.intersect(entity)

        if not isinstance(target, PlayerCharacter):
            entity.x = x_new
            entity.y = y_new
