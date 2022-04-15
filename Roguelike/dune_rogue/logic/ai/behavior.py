from abc import ABC


class Behavior(ABC):
    def __init__(self):
        pass

    def move(self, entity, mediator):
        raise NotImplementedError('move method is not implemented')

    @staticmethod
    def move_to_cell(entity, mediator, x_new, y_new):
        target = mediator.get_entity_at(x_new, y_new)

        entity.intersect(target)

        if not target.is_player:
            entity.x = x_new
            entity.y = y_new
