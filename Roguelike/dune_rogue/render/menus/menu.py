from abc import ABC

from dune_rogue.render.scene import Scene


class Menu(Scene, ABC):
    """Abstract class for menus"""
    def open(self):
        """Resets menu to initial state"""
        raise NotImplementedError('open function is not implemented')