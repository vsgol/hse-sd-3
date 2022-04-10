from dune_rogue.logic.states import State
from dune_rogue.render.menus.simple_menu import SimpleMenu
from dune_rogue.logic.actions import Action


class LvlSelectMenu(SimpleMenu):
    """Menu for selecting level to start from"""
    def __init__(self, loader):
        """
        :param loader: Level loader object which must be reconfigured after choice
        """
        super().__init__(
            options=[(f'Level {i}', None) for i in range(1, loader.number_of_levels + 1)] + [('Back', None)],
            title="Select level", menu_state=State.LEVEL_SELECTION)
        self.loader = loader

    def process_select(self):
        if self.selected_option == self.loader.number_of_levels:
            return State.MAIN_MENU
        self.loader.current_level = self.selected_option
        return State.LEVEL
