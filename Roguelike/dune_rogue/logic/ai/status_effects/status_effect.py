from abc import ABC

from dune_rogue.logic.ai.behavior import Behavior


class StatusEffect(Behavior, ABC):
    def __init__(self, behavior, duration=3):
        self.behavior = behavior
        self.duration = duration

    def move(self, entity, mediator):
        self.duration -= 1

    def purify_others(self):
        if isinstance(self.behavior, StatusEffect):
            self.behavior.purify_others()
            if self.behavior.duration <= 0:
                self.behavior = self.behavior.behavior
