from abc import ABC

from dune_rogue.logic.entities.acting_entity import CharacterEntity


class NPC(CharacterEntity, ABC):
    def __init__(self, x, y, glyph, behavior, is_friendly=False, stats=None, inventory=None):
        super().__init__(x, y, glyph, is_friendly, stats, inventory)
        self.behavior = behavior

    def update(self, mediator):
        self.behavior.move(self, mediator)
