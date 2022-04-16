import unittest

from dune_rogue.logic.entities.factory import EntityFactory
from dune_rogue.logic.entities.items.unfixed_crysknife_entity import UnfixedCrysknifeEntity
from dune_rogue.logic.entities.items.worn_stillsuit_entity import WornStillsuitEntity
from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.npcs.kangaroo_mouse import KangarooMouse
from dune_rogue.logic.entities.npcs.kit_fox import KitFox
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

        ent = factory.create_fox(1, 2)
        self.assertTrue(isinstance(ent, KitFox))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_mouse(1, 2)
        self.assertTrue(isinstance(ent, KangarooMouse))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_cielago(1, 2)
        self.assertTrue(isinstance(ent, Cielago))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_unfixed_crys(1, 2)
        self.assertTrue(isinstance(ent, UnfixedCrysknifeEntity))
        self.assertEqual((ent.x, ent.y), (1, 2))

        ent = factory.create_worn_stillsuit(1, 2)
        self.assertTrue(isinstance(ent, WornStillsuitEntity))
        self.assertEqual((ent.x, ent.y), (1, 2))

    def test_player_creating(self):
        factory = EntityFactory()

        player = factory.create_player_character(1, 2)
        self.assertTrue(isinstance(player, PlayerCharacter))
        self.assertEqual((player.x, player.y), (1, 2))


if __name__ == '__main__':
    unittest.main()
