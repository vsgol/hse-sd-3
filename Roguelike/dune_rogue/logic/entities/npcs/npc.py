from abc import ABC

from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.entities.player_character import PlayerCharacter


class NPC(CharacterEntity, ABC):
    """NPC character controlled by AI"""
    def __init__(self, x, y, glyph, behavior, is_friendly=False, stats=None, inventory=None):
        """
        :param x: NPC x position
        :param y: NPC y position
        :param glyph: glyph for displaying
        :param behavior: NPC behavior
        :param is_friendly: flag whether NPC is friendly
        :param stats: NPC stats
        :param inventory: NPC inventory
        """
        super().__init__(x, y, glyph, is_friendly, stats, inventory)
        self.behavior = behavior

    def update(self, mediator):
        self.behavior.move(self, mediator)


class Enemy(NPC, ABC):
    """NPC which can attack player and can be attacked by player"""
    def __init__(self, x, y, glyph, behavior, exp, stats=None, inventory=None):
        """
        :param x: Enemy x position
        :param y: Enemy y position
        :param glyph: glyph for displaying
        :param behavior: Enemy behavior
        :param exp: Amount of experience player gets after enemy death
        :param stats: Enemy stats
        :param inventory: Enemy inventory
        """
        super().__init__(x, y, glyph, behavior, False, stats, inventory)
        self.exp = exp

    def intersect(self, other):
        if isinstance(other, PlayerCharacter):
            other.make_damage(self.stats.attack)
