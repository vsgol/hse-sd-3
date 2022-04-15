from dune_rogue.logic.entities.acting_entity import ActingEntity


class ItemEntity(ActingEntity):
    def __init__(self, x, y, glyph, item):
        super().__init__(x, y, is_solid=False, glyph=glyph)
        self.item = item

    def update(self, mediator):
        pass
