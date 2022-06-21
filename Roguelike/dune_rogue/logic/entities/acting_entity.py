import random
from abc import ABC
from dune_rogue.logic.entities.game_entity import GameEntity


class ActingEntity(GameEntity, ABC):
    """Abstract class for entities which do some actions"""
    def update(self, mediator):
        """Performs entity action
        :argument mediator: reference to mediator which provides access to level and other entities
        """
        raise NotImplementedError('update method is not implemented')


class CharacterEntity(ActingEntity, ABC):
    """Abstract class for characters entities"""
    def __init__(self, x, y, glyph, is_friendly=False, stats=None, inventory=None):
        """
        :param is_friendly: flag indicates if entity is an enemy or not
        :param stats: character's statistics
        :param inventory: characters's inventory
        """
        super().__init__(x, y, is_solid=True, glyph=glyph)
        self.is_friendly = is_friendly
        self.stats = stats
        self.inventory = inventory

    def make_damage(self, damage):
        """Processes incoming damage
        :argument damage: amount of damage received
        """
        if damage == 0:
            return
        if self.stats.defence >= damage:
            diff = min(9, self.stats.defence - damage)
            if random.randint(1, 10) > diff:
                damage = 1
            else:
                damage = 0
        else:
            damage -= self.stats.defence
        self.stats.hp -= damage

        if self.stats.hp <= 0:
            self.is_alive = False

    def regen(self):
        """Regenerate health"""
        self.stats.hp += self.stats.regen
        self.stats.hp = min(self.stats.hp, self.stats.max_hp)
