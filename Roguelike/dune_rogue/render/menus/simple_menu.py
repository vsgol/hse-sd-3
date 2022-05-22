from abc import ABC

from dune_rogue.logic.actions import Action
from dune_rogue.render.menus.menu import Menu

from dune_rogue.render.color import Color, WHITE_COLOR, TITLE_COLOR


class SimpleMenu(Menu, ABC):
    """Simple menu with up/down navigation and selection"""
    def __init__(self, options, title, menu_state):
        """
        :param options: Menu options and corresponding states for selection
        :param title: Text displayed at the top
        :param menu_state: State corresponding to menu
        """
        self.options = options
        self.title = title
        self.menu_state = menu_state
        self.selected_option = 0

    def render(self):
        title_colors = [[TITLE_COLOR] * len(self.title)]

        options = list(map(lambda o: f' {o[0]}', self.options))
        options[self.selected_option] = '>>' + options[self.selected_option]
        options_colors = [[WHITE_COLOR] * len(o) for o in options]
        return [[[self.title]], [options]], [[title_colors], [options_colors]]

    def process_input(self, action):
        if action == Action.MOVE_UP:
            self.selected_option -= 1
        elif action == Action.MOVE_DOWN:
            self.selected_option += 1
        elif action == Action.SELECT:
            return self.process_select()
        self.selected_option = (self.selected_option + len(self.options)) % len(self.options)
        return self.menu_state

    def open(self):
        self.selected_option = 0

    def process_select(self):
        """Processes option selecting"""
        raise NotImplementedError('process_select function is not implemented')