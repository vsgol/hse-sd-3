from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.items.armors.worn_stillsuit import WornStillsuit
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class WornStillsuitEntity(ItemEntity):
    def __init__(self, x, y):
        super().__init__(x, y, glyph=Glyph('&', Color(200, 185, 130)), item=WornStillsuit())
