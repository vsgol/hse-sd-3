from abc import ABC

from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.entities.player_character import PlayerCharacter


class NPC(CharacterEntity, ABC):
    def __init__(self, x, y, glyph, behavior, is_friendly=False, stats=None, inventory=None):
        super().__init__(x, y, glyph, is_friendly, stats, inventory)
        self.behavior = behavior

    def update(self, mediator):
        self.behavior.move(self, mediator)


class Enemy(NPC, ABC):
    def __init__(self, x, y, glyph, behavior, exp, is_friendly=False, stats=None, inventory=None):
        super().__init__(x, y, glyph, behavior, is_friendly, stats, inventory)
        self.exp = exp

    def intersect(self, other):
        if isinstance(other, PlayerCharacter):
            other.make_damage(self.stats.attack)
