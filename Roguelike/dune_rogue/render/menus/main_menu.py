from dune_rogue.logic.states import State
from dune_rogue.render.menus.simple_menu import SimpleMenu


class MainMenu(SimpleMenu):
    """Main menu"""
    def __init__(self):
        super().__init__(options=[
            ('Start game', State.LEVEL),
            ('Dungeon mode', State.DUNGEON),
            ('Select level', State.LEVEL_SELECTION),
            ('Load game', State.LOAD),
            ('Exit', State.EXIT)
        ], title="DUNE ROGUE", menu_state=State.MAIN_MENU)

    def process_select(self):
        return self.options[self.selected_option][1]
