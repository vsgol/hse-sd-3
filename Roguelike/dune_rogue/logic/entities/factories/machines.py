from dune_rogue.logic.entities.factories.factory import EntityFactory
from dune_rogue.logic.entities.items.unfixed_crysknife_entity import UnfixedCrysknifeEntity
from dune_rogue.logic.entities.items.worn_stillsuit_entity import WornStillsuitEntity
from dune_rogue.logic.entities.npcs.brain import BrainInAJar
from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.npcs.cymek import Cymek
from dune_rogue.logic.entities.npcs.kangaroo_mouse import KangarooMouse
from dune_rogue.logic.entities.npcs.kit_fox import KitFox
from dune_rogue.logic.entities.npcs.valet import Valetbot


class MachinesFactory(EntityFactory):
    """Animals factory"""
    @staticmethod
    def create_aggressive(x, y):
        """Creates cymek entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized cymek entity
        """
        return Cymek(x, y)

    @staticmethod
    def create_coward(x, y):
        """Creates valetbot entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized valetbot entity
        """
        return Valetbot(x, y)

    @staticmethod
    def create_passive(x, y):
        """Creates brain in a jar entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized brain in a jar entity
        """
        return BrainInAJar(x, y)
