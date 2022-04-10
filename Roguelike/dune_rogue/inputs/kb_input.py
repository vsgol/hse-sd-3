import curses

from dune_rogue.logic.actions import Action


class InputHandler:
    """Keyboard input processing for ncurses"""
    def __init__(self, stdscr):
        """
        :param stdscr: ncurses interaction variable
        """
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.stdscr = stdscr

    def get_action(self):
        """ Maps pressed key to action
        :return: committed action
        """
        key = self.stdscr.getch()
        if key == ord('w'):
            return Action.MOVE_UP
        elif key == ord('s'):
            return Action.MOVE_DOWN
        elif key == ord('a'):
            return Action.MOVE_LEFT
        elif key == ord('d'):
            return Action.MOVE_RIGHT
        elif key == ord('i'):
            return Action.TOGGLE_INVENTORY
        elif key == ord('m'):
            return Action.TOGGLE_PAUSE
        elif key == 10 or key == 13:
            return Action.SELECT
        return None

