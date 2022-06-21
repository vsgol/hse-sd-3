import os
import random
import unittest
from copy import deepcopy
from pathlib import Path

from dune_rogue.logic.actions import Action
from dune_rogue.logic.entities.acting_entity import ActingEntity
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.items.item import InventoryItem
from dune_rogue.logic.levels.level import Level
from dune_rogue.logic.levels.loader import LevelLoader
from dune_rogue.logic.states import State
from dune_rogue.logic.stats import Stats
from dune_rogue.render.menus.error_message import ErrorMsg
from dune_rogue.render.menus.inventory_menu import InventoryMenu, _ITEM_TO_ENTITY_FUNC
from dune_rogue.render.menus.lvl_select_menu import LvlSelectMenu
from dune_rogue.render.menus.main_menu import MainMenu
from dune_rogue.render.menus.pause_menu import PauseMenu
from dune_rogue.render.menus.simple_menu import SimpleMenu


class MenusTest(unittest.TestCase):
    def check_neutral(self, menu, pause=False):
        for action in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.TOGGLE_INVENTORY, Action.PICK_PUT] + \
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
        self.assertEqual(menu.process_input(Action.SELECT), State.DUNGEON)
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
        self.assertEqual(menu.process_input(Action.SELECT), State.SWITCH_VISION)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.PAUSE_MENU)
        self.assertEqual(menu.process_input(Action.SELECT), State.MAIN_MENU)
        self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.PAUSE_MENU)
        self.assertEqual(menu.process_input(Action.TOGGLE_PAUSE), State.LEVEL)

    def test_inventory(self):
        player = PlayerCharacter(0, 0)
        cwd = os.path.realpath(__file__)
        path = Path(cwd)
        levels_dir = str(path.parent.absolute()) + os.sep + 'resources' + os.sep
        loader = LevelLoader()
        level = loader.load_from_file(levels_dir + 'level_1.lvl', player)
        n_items = 10
        menu = InventoryMenu(player, level)

        random.seed(0)
        for _ in range(n_items):
            player.inventory.add_item(
                InventoryItem(stats=Stats(0, random.randint(-5, 5), random.randint(-5, 5), 0), can_be_equipped=True))

        class DummyEntity(ActingEntity):
            def update(self, mediator):
                pass

        _ITEM_TO_ENTITY_FUNC[InventoryItem] = lambda x, y: DummyEntity(x, y, False, None)
        stats_player = deepcopy(player.stats)

        self.assertEqual(menu.selected_option, 0)

        for action in [Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            self.assertEqual(menu.process_input(action), menu.menu_state)
            self.assertEqual(menu.selected_option, 0)

        for i in range(1, n_items * 3):
            self.assertEqual(menu.process_input(Action.MOVE_DOWN), State.INVENTORY)
            self.assertEqual(menu.selected_option, i % n_items)
            self.assertEqual(menu.process_input(Action.SELECT), State.INVENTORY)
            self.assertEqual(player.stats, stats_player + player.inventory.items[i % n_items].stats)
            self.assertEqual(menu.process_input(Action.SELECT), State.INVENTORY)
            self.assertEqual(player.stats, stats_player)

        menu.open()
        self.assertEqual(menu.selected_option, 0)
        for i in range(n_items * 3 - 1, -1, -1):
            self.assertEqual(menu.process_input(Action.MOVE_UP), State.INVENTORY)
            self.assertEqual(menu.selected_option, i % n_items)
            self.assertEqual(menu.process_input(Action.SELECT), State.INVENTORY)
            self.assertEqual(player.stats, stats_player + player.inventory.items[i % n_items].stats)
            self.assertEqual(menu.process_input(Action.SELECT), State.INVENTORY)
            self.assertEqual(player.stats, stats_player)

        for i in range(1, n_items + 1):
            self.assertEqual(menu.process_input(Action.PICK_PUT), State.INVENTORY)
            self.assertEqual(len(player.inventory.items), n_items - i)
            self.assertEqual(len(level.acting_entities), i + 1)
        for ent in level.acting_entities:
            self.assertEqual((player.x, player.y), (ent.x, ent.y))


if __name__ == '__main__':
    unittest.main()
