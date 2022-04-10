from dune_rogue.logic.states import State
from dune_rogue.render.menus.simple_menu import SimpleMenu
from dune_rogue.logic.actions import Action


class ErrorMsg(SimpleMenu):
    """Message for reporting save/load failures"""
    def __init__(self, next_state):
        """
        :param next_state: Next to go after pressing 'OK'
        """
        super().__init__(options=[
            ('OK', next_state),
        ], title="Something went wrong while tying to load/save game (press Enter to continue)", menu_state=State.ERR)

    def process_select(self):
        return self.options[self.selected_option][1]
