from dune_rogue.logic.ai.behavior import Behavior
from dune_rogue.logic.ai.coward import CowardBehavior
from dune_rogue.logic.entities.player_character import PlayerCharacter


class PassiveBehavior(Behavior):
    """Entity stays at its position and attacks player if it can"""

    def act(self, entity, mediator):
        player_coord = mediator.level.player.coord
        entity_coord = entity.coord

        coord = entity_coord
        if self.acceptable_position(player_coord, entity_coord):
            coord = player_coord

        self.move_to_cell(entity, mediator, coord)
