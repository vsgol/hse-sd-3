from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.items.usable.healing_potion import HealingPotion
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class HealingPotionEntity(ItemEntity):
    """Healing potion entity"""
    def __init__(self, x, y):
        super().__init__(x, y, glyph=Glyph('6', Color(255, 0, 0)), item=HealingPotion())