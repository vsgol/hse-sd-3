import curses

from dune_rogue.inputs.kb_input import InputHandler


class Drawer:
    """Class for drawing everything"""
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.curs_set(0)
        self.input_handler = InputHandler(self.stdscr)

    def deinit(self):
        """Deinitialize ncurses"""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    @staticmethod
    def rgb_to_ruses(r, g, b):
        """ Converts RGB values to ncurses colors
        :argument r: red
        :argument g: green
        :argument b: blue
        :return: converted colors
        """
        return int(r / 255 * 999), int(g / 255 * 999), int(b / 255 * 999)

    def render_scene(self, symbols_frame, colors_frame):
        """ Renders scene
        :argument symbols_frame: symbols to be drawn
        :argument colors_frame: colors for symbols
        """
        self.stdscr.erase()
        new_color_id = curses.COLORS - 1
        new_pair_id = 255
        colors_mapping = {}
        y_max_prev = 0

        for n, row in enumerate(symbols_frame):
            x_max_prev = 0
            for m, col in enumerate(row):
                colors = colors_frame[n][m]

                cur_x_max = 0
                cur_y_max = 0

                for i, r in enumerate(col):
                    for j, c in enumerate(r):
                        if curses.can_change_color():
                            color_tuple = colors[i][j].R, colors[i][j].G, colors[i][j].B
                            if color_tuple not in colors_mapping:
                                colors_mapping[color_tuple] = (new_color_id, new_pair_id)
                                curses.init_color(new_color_id,
                                                  *self.rgb_to_ruses(colors[i][j].R, colors[i][j].G, colors[i][j].B))
                                curses.init_pair(new_pair_id, new_color_id, curses.COLOR_BLACK)
                                new_color_id -= 1
                                new_pair_id -= 1
                            color_id, pair_id = colors_mapping[color_tuple]
                            self.stdscr.addstr(y_max_prev + i, x_max_prev + j, c, curses.color_pair(pair_id))
                        else:
                            self.stdscr.addstr(y_max_prev + i, x_max_prev + j, c)

                        cur_x_max = max(cur_x_max, j)
                    cur_y_max = max(cur_y_max, i)
                x_max_prev = max(x_max_prev, cur_x_max + 2)
                y_max_prev = max(y_max_prev, cur_y_max + 2)

        self.stdscr.refresh()
