from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.items.weapons.unfixed_crysknife import UnfixedCrysknife
from dune_rogue.render.color import Color
from dune_rogue.render.glyph import Glyph


class UnfixedCrysknifeEntity(ItemEntity):
    def __init__(self, x, y):
        super().__init__(x, y, glyph=Glyph('|', Color(255, 255, 200)), item=UnfixedCrysknife())