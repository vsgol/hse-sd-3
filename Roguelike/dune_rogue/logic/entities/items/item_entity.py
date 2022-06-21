from dune_rogue.logic.entities.acting_entity import ActingEntity


class ItemEntity(ActingEntity):
    """Item entity which can be picked up from level"""
    def __init__(self, x, y, glyph, item):
        """
        :param x: entity x coordinate
        :param y: entity y coordinate
        :param glyph: glyph for displaying
        :param item: corresponding item
        """
        super().__init__(x, y, is_solid=False, glyph=glyph)
        self.item = item

    def update(self, mediator):
        pass
