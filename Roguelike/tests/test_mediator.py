import unittest

from dune_rogue.logic.coordinate import Coordinate
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.entities.static_entities import FloorEntity, WallEntity
from dune_rogue.logic.levels.mediator import LevelMediator


class MediatorTest(unittest.TestCase):
    class DummyLevel:
        def __init__(self, w, h, static_entities, acting_entities):
            self.w = w
            self.h = h
            self.static_entities = static_entities
            self.acting_entities = acting_entities

    def test_shape(self):
        mediator = LevelMediator(MediatorTest.DummyLevel(10, 5, [], []))
        self.assertEqual(mediator.get_level_shape(), (10, 5))
        mediator = LevelMediator(MediatorTest.DummyLevel(5, 10, [], []))
        self.assertEqual(mediator.get_level_shape(), (5, 10))

    def test_all_entities(self):
        mediator = LevelMediator(MediatorTest.DummyLevel(0, 0, [1, 2, 3, 4], [5, 6]))
        self.assertEqual(mediator.get_all_entities(), ([1, 2, 3, 4], [5, 6]))

    def test_entity_at(self):
        mediator = LevelMediator(MediatorTest.DummyLevel(2, 2, [
            [FloorEntity(0, 0), WallEntity(1, 0)],
            [WallEntity(0, 1), WallEntity(1, 1)],
        ], [PlayerCharacter(0, 0)]))

        self.assertTrue(isinstance(mediator.get_entity_at(Coordinate(0, 0)), PlayerCharacter))
        self.assertTrue(isinstance(mediator.get_entity_at(Coordinate(0, 1)), WallEntity))
        self.assertTrue(isinstance(mediator.get_entity_at(Coordinate(1, 0)), WallEntity))
        self.assertTrue(isinstance(mediator.get_entity_at(Coordinate(1, 1)), WallEntity))


if __name__ == '__main__':
    unittest.main()
