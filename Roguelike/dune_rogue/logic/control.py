import os
from pathlib import Path
from random import randrange

from dune_rogue.logic.levels.loader import LevelLoader, LevelGenerator
from dune_rogue.logic.entities.factory import EntityFactory
from dune_rogue.logic.states import State
from dune_rogue.render.menus.inventory_menu import InventoryMenu
from dune_rogue.render.menus.main_menu import MainMenu
from dune_rogue.render.menus.pause_menu import PauseMenu
from dune_rogue.render.menus.lvl_select_menu import LvlSelectMenu
from dune_rogue.other.pkl_utils import save_pkl, load_pkl
from dune_rogue.render.menus.error_message import ErrorMsg

_MIN_LEVEL_SIZE = 15
_MAX_LEVEL_SIZE = 40


class GameControl:
    """Game controller"""
    def __init__(self, drawer):
        """
        :param drawer: component for drawing
        """
        self.level_loader = LevelLoader()
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.level_selection = LvlSelectMenu(self.level_loader)
        self.err_msg = ErrorMsg(State.MAIN_MENU)
        self.player = EntityFactory().create_player_character(0, 0)
        self.level = None
        self.inventory = InventoryMenu(self.player, self.level)
        self.drawer = drawer
        self.input_handler = drawer.input_handler
        self.state = State.MAIN_MENU
        self.new_state = None
        self.current_scene = self.main_menu

        self.save_dir = str(Path.home()) + os.sep + '.dune_rogue' + os.sep
        self.save_lvl = self.save_dir + 'lvl_save.pkl'
        self.save_loader = self.save_dir + 'loader_save.pkl'

    def save_game(self):
        """ Saves game
        :returns: whether save was successful
        """
        try:
            os.makedirs(self.save_dir, exist_ok=True)
            save_pkl(self.save_lvl, self.level)
            save_pkl(self.save_loader, self.level_loader)
        except:
            return False
        return True

    def load_game(self):
        """ Loads game
        :returns: whether load was successful
        """
        try:
            self.level = load_pkl(self.save_lvl)
            self.level_loader = load_pkl(self.save_loader)
            self.level_selection.loader = self.level_loader
            self.player = self.level.player
            self.inventory = InventoryMenu(self.player, self.level)
        except:
            return False
        return True

    def go_to_next_level(self):
        try:
            self.level_loader.set_sizes(randrange(_MIN_LEVEL_SIZE, _MAX_LEVEL_SIZE),
                                        randrange(_MIN_LEVEL_SIZE, _MAX_LEVEL_SIZE))
            self.level = self.level_loader.build(self.player)
            self.inventory = InventoryMenu(self.player, self.level)
        except:
            self.new_state = State.ERR
            self.err_msg = ErrorMsg(State.MAIN_MENU)
        if self.level is None:
            self.new_state = State.MAIN_MENU

    def start_new_game(self):
        self.player = EntityFactory().create_player_character(0, 0)
        self.level_loader = LevelLoader()
        self.level_selection.loader = self.level_loader
        self.level_loader.reset()
        try:
            self.level = self.level_loader.build(self.player)
            self.inventory = InventoryMenu(self.player, self.level)
        except:
            self.new_state = State.ERR
            self.err_msg = ErrorMsg(State.MAIN_MENU)

    def start_dungeon(self):
        self.new_state = State.LEVEL
        self.player = EntityFactory().create_player_character(0, 0)
        self.level_loader = LevelGenerator()
        self.level_loader.set_sizes(randrange(_MIN_LEVEL_SIZE, _MAX_LEVEL_SIZE),
                                    randrange(_MIN_LEVEL_SIZE, _MAX_LEVEL_SIZE))
        self.level = self.level_loader.build(self.player)
        self.inventory = InventoryMenu(self.player, self.level)

    def load_level(self):
        self.player = EntityFactory().create_player_character(0, 0)
        try:
            self.level = self.level_loader.build(self.player)
            self.inventory = InventoryMenu(self.player, self.level)
        except:
            self.new_state = State.ERR
            self.err_msg = ErrorMsg(State.LEVEL_SELECTION)

    def exit_to_main_menu(self):
        if self.save_game():
            self.new_state = State.MAIN_MENU
        else:
            self.new_state = State.ERR
            self.err_msg = ErrorMsg(State.MAIN_MENU)
        self.level_loader = LevelLoader()
        self.level_selection.loader = self.level_loader

    def process_load_save(self):
        if self.new_state == State.LOAD:
            if self.load_game():
                self.new_state = State.LEVEL
            else:
                self.new_state = State.ERR
                self.err_msg = ErrorMsg(self.state)
        elif self.new_state == State.SAVE:
            if self.save_game():
                self.new_state = State.LEVEL
            else:
                self.new_state = State.ERR
                self.err_msg = ErrorMsg(self.state)

    def process_new_state(self):
        if self.new_state == State.LEVEL:
            self.current_scene = self.level
        elif self.new_state == State.MAIN_MENU:
            if self.new_state != self.state:
                self.main_menu.open()
            self.current_scene = self.main_menu
        elif self.new_state == State.PAUSE_MENU:
            if self.new_state != self.state:
                self.pause_menu.open()
            self.current_scene = self.pause_menu
        elif self.new_state == State.LEVEL_SELECTION:
            if self.new_state != self.state:
                self.level_selection.open()
            self.current_scene = self.level_selection
        elif self.new_state == State.ERR:
            self.current_scene = self.err_msg
        elif self.new_state == State.INVENTORY:
            self.current_scene = self.inventory

    def start(self):
        """Runs game loop"""
        try:
            while True:
                self.drawer.render_scene(*self.current_scene.render())
                action = None
                while action is None:
                    action = self.input_handler.get_action()

                self.new_state = self.current_scene.process_input(action)

                # If level finished load next otherwise go to the main menu
                if self.level and self.level.is_finished:
                    self.go_to_next_level()
                # Starting new game
                if self.state == State.MAIN_MENU and self.new_state == State.LEVEL:
                    self.start_new_game()
                elif self.state == State.MAIN_MENU and self.new_state == State.DUNGEON:
                    self.start_dungeon()
                # Loading selected level
                elif self.state == State.LEVEL_SELECTION and self.new_state == State.LEVEL:
                    self.load_level()
                # Exiting to main menu and trying to save game
                elif self.state == State.PAUSE_MENU and self.new_state == State.MAIN_MENU:
                    self.exit_to_main_menu()

                self.process_load_save()
                if self.new_state == State.EXIT:
                    break
                self.process_new_state()

                self.state = self.new_state

        except KeyboardInterrupt:
            pass
        finally:
            self.drawer.deinit()
