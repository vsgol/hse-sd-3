from abc import ABC

from dune_rogue.logic.ai.coward import CowardBehavior, move_to_coward_position


class BehaviorState(ABC):
    """Behavior state class"""

    def move(self, entity, mediator):
        """ Make decision
        :argument entity: game entity with this state
        :argument mediator: level mediator
        """
        assert False  # move is not implemented

    def update_state(self, entity):
        """ Updates entities behavior
        :argument entity: game entity with this behavior
        """
        pass


class NormalState(BehaviorState):
    """Normal behavior state"""

    def move(self, entity, mediator):
        """ Make decision
        :argument entity: game entity with this state
        :argument mediator: level mediator
        """
        entity.behavior.act(entity, mediator)

    def update_state(self, entity):
        """ Updates entities behavior
        :argument entity: game entity with this behavior
        """
        if 3 * entity.stats.hp <= entity.stats.max_hp:
            entity.behavior.current_state = PanicState()


class PanicState(BehaviorState):
    """Panic behavior state"""

    def move(self, entity, mediator):
        """ Make decision
        :argument entity: game entity with this state
        :argument mediator: level mediator
        """
        move_to_coward_position(entity.behavior, entity, mediator)

    def update_state(self, entity):
        """ Updates entities behavior
        :argument entity: game entity with this behavior
        """
        if 3 * entity.stats.hp > entity.stats.max_hp:
            entity.behavior.current_state = NormalState()

