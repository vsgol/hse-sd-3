import npyscreen
import curses


class MainMenuForm(npyscreen.FormWithMenus):
    def __init__(self, level=None, *args, **keywords):
        super().__init__(*args, **keywords)
        if level is None:
            self.level = 1
        else:
            self.level = level
        self.exit = False

    def create(self):
        self.m = self.add_menu(name="Main Menu", shortcut="^M")
        self.m.addItemsFromList([
            ("Start", self.when_start_game, "s"),
            ("Exit", self.when_exit, "e"),
        ])
        self.m_level = self.m.addNewSubmenu("Choose level", "l")
        self.m_level.addItemsFromList([
            ("level 1", self.when_level_1, "1"),
            ("level 2", self.when_level_2, "2"),
            ("level 3", self.when_level_3, "3"),
        ])

    def when_start_game(self):
        self.level = 1
        print(self.level)

    def when_exit(self):
        self.exit = True

    def when_level_1(self):
        self.level = 1

    def when_level_2(self):
        self.level = 2

    def when_level_3(self):
        self.level = 3

    def afterEditing(self):
        if self.exit:
            self.parentApp.setNextForm(None)
        else:
            self.parentApp.setNextForm("level")


class LevelRepresentation(npyscreen.Form):
    def __init__(self, field=None, stats=None, message=None, *args, **keywords):
        super().__init__(*args, **keywords)

    def create(self):
        self.field = ['####', '###$', '^###', '####']
        self.stats = [f'EX: {0}', f'HP: {100}']
        self.message = ['line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6', 'line 7']

        self.switch_to_item_menu = False

        field_box = self.add(
            npyscreen.BoxTitle,
            name="Field: ",
            max_width=70,
            relx=2,
            max_height=26,
            scroll_exit=False,
            exit_right=True
        )
        field_box.entry_widget.scroll_exit = False
        field_box.values = self.field

        message_box = self.add(
            npyscreen.BoxTitle,
            name="Message:",
            rely=2,
            relx=74,
            max_width=40,
            max_height=7,
            # scroll_exit=False,
            slow_scroll=True,
            exit_right=True
        )
        message_box.entry_widget.scroll_exit = True
        message_box.values = self.message

        stats_box = self.add(
            npyscreen.BoxTitle,
            name="Stats:",
            rely=10,
            relx=74,
            max_width=40,
            max_height=18,
            scroll_exit=True,
            exit_right=True,
            exit_left=True
        )
        # stats_box.entry_widget.scroll_exit = True
        stats_box.values = self.stats

        self.add_handlers({
            "i": self.key_handler,
            "w": self.key_handler,
            "a": self.key_handler,
            "s": self.key_handler,
            "d": self.key_handler
        })

    def key_handler(self, key):
        if key == 105:
            # item menu
            print(105, 'i')
            self.editing = False
            self.switch_to_item_menu = True
            # self.afterEditing()
            # self.parentApp.setNextForm("MAIN")
            self.parentApp.switchForm("item_menu")
        elif key == 119:
            print(119, 'w')
        elif key == 97:
            print(97, 'a')
        elif key == 115:
            print(115, 's')
        elif key == 100:
            print(100, 'd')
        # self.display()

    def afterEditing(self):
        if self.switch_to_item_menu:
            self.parentApp.setNextForm("item_menu")
            self.switch_to_item_menu = False
        else:
            self.parentApp.setNextForm("MAIN")


class ItemMenu(npyscreen.Form):
    def __init__(self, items=None, item_stats=None, stats=None, *args, **keywords):
        super().__init__(*args, **keywords)

    def create(self):
        self.items = ['some item 1', 'some item 2', 'some item 3']

        field_box = self.add(
            npyscreen.BoxTitle,
            name="Inventory: ",
            max_width=60,
            relx=2,
            max_height=26,
            scroll_exit=False,
            exit_right=True
        )
        field_box.entry_widget.scroll_exit = False
        field_box.values = self.items

    def afterEditing(self):
        self.parentApp.setNextForm("level")


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        # npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.registerForm('MAIN', MainMenuForm())
        self.registerForm("level", LevelRepresentation())
        self.registerForm("item_menu", ItemMenu())


if __name__ == '__main__':
    TestApp = MyApplication().run()
