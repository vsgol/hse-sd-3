from dune_rogue.logic.states import State
from dune_rogue.render.menus.simple_menu import SimpleMenu
from dune_rogue.logic.actions import Action


class PauseMenu(SimpleMenu):
    """Pause menu"""
    def __init__(self):
        super().__init__(options=[
            ('Continue', State.LEVEL),
            ('Save', State.SAVE),
            ('Exit', State.MAIN_MENU)
        ], title="Game is paused", menu_state=State.PAUSE_MENU)

    def process_input(self, action):
        if action == Action.TOGGLE_PAUSE:
            return State.LEVEL
        return super().process_input(action)

    def process_select(self):
        return self.options[self.selected_option][1]
