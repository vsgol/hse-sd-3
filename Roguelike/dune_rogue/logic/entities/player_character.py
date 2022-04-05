from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.inventory import Inventory
from dune_rogue.logic.stats import PlayerStats
from dune_rogue.render.color import Color, WHITE_COLOR
from dune_rogue.render.glyph import Glyph


DEFAULT_PLAYER_STATS = PlayerStats(15, 1, 2, 15)


class PlayerCharacter(CharacterEntity):
    """Player character class"""
    def __init__(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        """
        super().__init__(x, y, is_friendly=True,
                         glyph=Glyph('@', WHITE_COLOR),
                         inventory=Inventory(60), stats=DEFAULT_PLAYER_STATS)

    def update(self, mediator):
        """Performs entity action
        :argument mediator: reference to mediator which provides access to level and other entities
        """
        # For now is empty as player character control is separated
        # But this method might be used for some status effects (e.g. regeneration, bleeding)
        pass
