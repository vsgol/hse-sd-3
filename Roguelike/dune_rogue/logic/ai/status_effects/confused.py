from dune_rogue.logic.ai.random import RandomBehavior
from dune_rogue.logic.ai.status_effects.status_effect import StatusEffect


class Confused(StatusEffect):
    """Confusion status effect. Agent starts to move randomly"""
    def __init__(self, behavior, duration=3):
        super().__init__(behavior, duration)
        self.rnd_behavior = RandomBehavior()

    def move(self, entity, mediator):
        super().move(entity, mediator)
        self.rnd_behavior.move(entity, mediator)
