import random

from dune_rogue.logic.ai.status_effects.confused import Confused
from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.inventory import Inventory
from dune_rogue.logic.items.armors.armor import Armor
from dune_rogue.logic.items.weapons.weapon import Weapon
from dune_rogue.logic.stats import PlayerStats
from dune_rogue.render.color import Color, WHITE_COLOR
from dune_rogue.render.glyph import Glyph

DEFAULT_PLAYER_STATS = lambda: PlayerStats(15, 1, 1, 15)
CONFUSE_CHANCE = 0.25


class PlayerCharacter(CharacterEntity):
    """Player character class"""

    def __init__(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        """
        super().__init__(x, y, is_friendly=True,
                         glyph=Glyph('@', Color(155, 155, 155)),
                         inventory=Inventory(60), stats=DEFAULT_PLAYER_STATS())
        self.is_player = True
        self.weapon = None
        self.armor = None

    def update(self, mediator):
        """Performs entity action
        :argument mediator: reference to mediator which provides access to level and other entities
        """
        # For now is empty as player character control is separated
        # But this method might be used for some status effects (e.g. regeneration, bleeding)
        pass

    def intersect(self, other):
        if isinstance(other, CharacterEntity) and not other.is_friendly:
            other.make_damage(self.stats.attack)
            if random.random() < CONFUSE_CHANCE:
                other.behavior = Confused(other.behavior)

    def equip_item(self, item):
        """Equip item
        :argument item: argument to be equipped
        """
        if isinstance(item, Weapon):
            if self.weapon:
                self.unequip_item(self.weapon)
            self.weapon = item
        elif isinstance(item, Armor):
            if self.armor:
                self.unequip_item(self.armor)
            self.armor = item
        self.stats.add_stats(item.get_bonuses())
        item.equip()

    def unequip_item(self, item):
        """Unequip item
        :argument item: argument to be unequipped
        """
        if item is self.weapon:
            self.weapon = None
        elif item is self.armor:
            self.armor = None
        self.stats.remove_stats(item.get_bonuses())
        item.unequip()

    def use_item(self, item_id):
        """Uses item
        :argument item_id: id of the item to be used
        """
        item = self.inventory.items[item_id]
        if not item.usable:
            return
        self.stats.add_stats(item.get_bonuses())
        self.inventory.remove_item(item_id)
