import unittest

from dune_rogue.logic.actions import Action
from dune_rogue.logic.states import State
from dune_rogue.render.menus.error_message import ErrorMsg
from dune_rogue.render.menus.lvl_select_menu import LvlSelectMenu
from dune_rogue.render.menus.main_menu import MainMenu
from dune_rogue.render.menus.pause_menu import PauseMenu
from dune_rogue.render.menus.simple_menu import SimpleMenu


class MenusTest(unittest.TestCase):
    def check_neutral(self, menu, pause=False):
        for action in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.TOGGLE_INVENTORY] + \
                      ([Action.TOGGLE_PAUSE] if not pause else []):
            self.assertEqual(menu.process_input(action), menu.menu_state)
            self.assertEqual(menu.selected_option, 0)

    def test_simple_menu(self):
        n_options = 20
        menu_state = "MENU_STATE"

        class DummyMenu(SimpleMenu):
            def __init__(self):
                super().__init__([(f'Option {i}', i) for i in range(n_options)], "title", menu_state)

            def process_select(self):
                return self.options[self.selected_option][1]

        menu = DummyMenu()
        self.assertEqual(menu.selected_option, 0)

        self.check_neutral(menu)

        for i in range(1, n_options * 3):
            self.assertEqual(menu.process_input(Action.MOVE_DOWN), menu_state)
            self.assertEqual(menu.selected_option, i % n_options)
            self.assertEqual(menu.process_input(Action.SELECT), i % n_options)
            self.assertEqual(menu.process_select(), i % n_options)
        menu.open()
        self.assertEqual(menu.selected_option, 0)
        for i in range(n_options * 3 - 1, -1, -1):
            self.assertEqual(menu.process_input(Action.MOVE_UP), menu_state)
            self.assertEqual(menu.selected_option, i % n_options)
            self.assertEqual(menu.process_input(Action.SELECT), i % n_options)
            self.assertEqual(menu.process_select(), i % n_options)

    def test_err(self):
        state = "Next"
        msg = ErrorMsg(state)
        self.check_neutral(msg)
        for action in [Action.MOVE_DOWN, Action.MOVE_UP]:
            self.assertEqual(msg.process_input(action), msg.menu_state)
            self.assertEqual(msg.selected_option, 0)
        self.assertEqual(msg.process_input(Action.SELECT), state)

    def test_lvl_select(self):
        n_levels = 5

        class DummyLoader:
            number_of_levels = n_levels
            current_level = 0

        loader = DummyLoader()
        menu = LvlSelectMenu(loader)
        self.check_neutral(menu)

        for i in range(n_levels):
            self.assertEqual(menu.process_input(Action.SELECT), State.LEVEL)
            self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.LEVEL_SELECTION)
            self.assertEqual(loader.current_level, i)
        self.assertEqual(menu.process_input(Action.SELECT), State.MAIN_MENU)

    def test_main_menu(self):
        menu = MainMenu()
        self.check_neutral(menu)

        self.assertEqual(menu.process_input(Action.SELECT), State.LEVEL)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.MAIN_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.LEVEL_SELECTION)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.MAIN_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.LOAD)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.MAIN_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.EXIT)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.MAIN_MENU)

    def test_pause_menu(self):
        menu = PauseMenu()
        self.check_neutral(menu, True)

        self.assertEqual(menu.process_input(Action.SELECT), State.LEVEL)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.PAUSE_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.SAVE)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.PAUSE_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.MAIN_MENU)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.PAUSE_MENU)
        self.assertEqual(menu.process_input(Action.TOGGLE_PAUSE), State.LEVEL)


if __name__ == '__main__':
    unittest.main()
