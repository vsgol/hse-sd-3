import random
from abc import ABC

from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.entities.player_character import PlayerCharacter


class NPC(CharacterEntity, ABC):
    """NPC character controlled by AI"""
    def __init__(self, x, y, glyph, behavior, is_friendly, stats, inventory=None):
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
        self.behavior = self.behavior.new_behavior(self)


class Enemy(NPC, ABC):
    """NPC which can attack player and can be attacked by player"""
    def __init__(self, x, y, glyph, behavior, exp, stats, inventory=None):
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


class Replicating(Enemy):
    """Replecating enemy"""
    def __init__(self, x, y, glyph, behavior, exp, replication_chance, stats, inventory=None):
        """
        :param x: Enemy x position
        :param y: Enemy y position
        :param glyph: glyph for displaying
        :param behavior: Enemy behavior
        :param exp: Amount of experience player gets after enemy death
        :param replication_chance: chance to be replicated
        :param stats: Enemy stats
        :param inventory: Enemy inventory
        """
        super().__init__(x, y, glyph, behavior, exp, stats, inventory)
        self.replication_chance = replication_chance

    def replicates_now(self):
        """Tells whether to replicate or not"""
        return random.random() < self.replication_chance

    def update(self, mediator):
        if self.replicates_now():
            self.clone(mediator)
        self.behavior.move(mediator)

    def clone(self, mediator):
        """Clones self and puts copy to level"""
        raise NotImplementedError('clone is not implemented')
