import unittest

from dune_rogue.logic.entities.factory import EntityFactory
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.entities.static_entities import *


class EntFactoryTest(unittest.TestCase):
    def test_creating(self):
        factory = EntityFactory()

        ent = factory.create_wall(1, 2)
        self.assertTrue(isinstance(ent, WallEntity))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_floor(1, 2)
        self.assertTrue(isinstance(ent, FloorEntity))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_finish(1, 2)
        self.assertTrue(isinstance(ent, LevelFinishEntity))
        self.assertEqual((ent.x, ent.y), (1, 2))

    def test_player_creating(self):
        factory = EntityFactory()

        player = factory.create_player_character(1, 2)
        self.assertTrue(isinstance(player, PlayerCharacter))
        self.assertEqual((player.x, player.y), (1, 2))


if __name__ == '__main__':
    unittest.main()
