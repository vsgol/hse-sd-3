from abc import ABC

from dune_rogue.logic.ai.behavior import Behavior


class StatusEffect(Behavior, ABC):
    """Base class for wrapping behaviors to implement status effects on behavior. Removed after duration ends"""
    def __init__(self, behavior, duration=3):
        """
        :param behavior: behavior to be wrapped
        :param duration: number of updates before effect ends
        """
        super().__init__()
        self.behavior = behavior
        self.duration = duration

    def move(self, entity, mediator):
        self.duration -= 1

    def purify_others(self):
        """Remove all wrapped status effects which durations ended"""
        if isinstance(self.behavior, StatusEffect):
            self.behavior.purify_others()
            if self.behavior.duration <= 0:
                self.behavior = self.behavior.behavior
