from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.entities.player_character import PlayerCharacter


class PassiveBehavior(Behavior):
    """Entity stays at its position and attacks player if it can"""
    def __init__(self, previous=None):
        super().__init__(previous)

    def new_behavior(self, entity):
        if 3 * entity.stats.hp <= entity.stats.max_hp:
            return CowardBehavior(previous=self)
        return self

    def move(self, entity, mediator):
        x_player = mediator.level.player.x
        y_player = mediator.level.player.y
        x_entity = entity.x
        y_entity = entity.y

        x, y = x_entity, y_entity
        if (x_player == x_entity and abs(y_player - y_entity) <= 1 or
                y_player == y_entity and abs(x_player - x_entity) <= 1):
            x, y = x_player, y_player

        self.move_to_cell(entity, mediator, x, y)
