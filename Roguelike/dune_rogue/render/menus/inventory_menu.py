from dune_rogue.logic.actions import Action
from dune_rogue.logic.entities.factory import EntityFactory
from dune_rogue.logic.items.armors.worn_stillsuit import WornStillsuit
from dune_rogue.logic.items.weapons.unfixed_crysknife import UnfixedCrysknife
from dune_rogue.logic.states import State
from dune_rogue.render.menus.menu import Menu

from dune_rogue.render.color import Color, WHITE_COLOR


MAX_DESCR_LINE_LEN = 10
_ITEM_TO_ENTITY_FUNC = {
    UnfixedCrysknife: EntityFactory.create_unfixed_crys,
    WornStillsuit: EntityFactory.create_worn_stillsuit,
}


class InventoryMenu(Menu):
    """Inventory menu"""
    def __init__(self, player, level):
        """
        :param player: Player character reference
        :param level: Level reference
        """
        self.player = player
        self.level = level
        self.title = 'Inventory'
        self.menu_state = State.INVENTORY
        self.selected_option = 0

    def render(self):
        title_colors = [[Color(249, 213, 162)] * len(self.title)]

        if len(self.player.inventory.items) != 0:
            options = list(map(lambda o: f' {o.name}   {"*" if o.is_equipped else " "} ', self.player.inventory.items))
            options[self.selected_option] = '>>' + options[self.selected_option]
            options[self.selected_option] = options[self.selected_option][:-4] + options[self.selected_option][-2:]
        else:
            options = ['Inventory is empty    ']
        options_colors = [[WHITE_COLOR] * len(o) for o in options]

        selected_description = ['| Inventory capacity:',
                                f'|  {self.player.inventory.weight}/{self.player.inventory.capacity}']
        if len(self.player.inventory.items) != 0:
            selected_item = self.player.inventory.items[self.selected_option]
            splited = selected_item.description.split()
            bonuses = selected_item.get_bonuses_str()
            selected_description += ['|', f'| Type:', f'|  {selected_item.item_type}']
            selected_description += ['|', f'| Weight:', f'|  {selected_item.weight}']
            if len(bonuses) > 0:
                selected_description += ['|', f'| Bonuses:', f'|  {bonuses}']
            selected_description += ['|', '| Description:']
            selected_description += ['|  ' + ' '.join(splited[i * MAX_DESCR_LINE_LEN:(i + 1) * MAX_DESCR_LINE_LEN]) for
                                     i
                                     in range(len(selected_item.description.split()) // MAX_DESCR_LINE_LEN +
                                              (len(selected_item.description.split()) % MAX_DESCR_LINE_LEN != 0))
                                     ]
        descr_colors = [[WHITE_COLOR] * len(d) for d in selected_description]

        stats_text = str(self.player.stats)

        return [[[self.title]], [options, selected_description], [[stats_text]]],\
               [[title_colors], [options_colors, descr_colors], [[[WHITE_COLOR] * len(stats_text)]]]

    def process_input(self, action):
        if action == Action.MOVE_UP:
            self.selected_option -= 1
        elif action == Action.MOVE_DOWN:
            self.selected_option += 1
        elif action == Action.TOGGLE_INVENTORY:
            return State.LEVEL
        elif action == Action.SELECT:
            if len(self.player.inventory.items) != 0:
                selected_item = self.player.inventory.items[self.selected_option]
                if selected_item.can_be_equipped:
                    if not selected_item.is_equipped:
                        self.player.equip_item(selected_item)
                    else:
                        self.player.unequip_item(selected_item)
        elif action == Action.PICK_PUT:
            if len(self.player.inventory.items) != 0:
                selected_item = self.player.inventory.items[self.selected_option]
                if selected_item.is_equipped:
                    self.player.unequip_item(selected_item)
                self.level.acting_entities.append(_ITEM_TO_ENTITY_FUNC[type(selected_item)](self.player.x, self.player.y))
                self.player.inventory.remove_item(self.selected_option)

        if len(self.player.inventory.items) == 0:
            self.selected_option = 0
        else:
            self.selected_option = (self.selected_option + len(self.player.inventory.items)) % len(self.player.inventory.items)
        return self.menu_state

    def open(self):
        self.selected_option = 0

    def process_select(self):
        """Processes option selecting"""
        raise NotImplementedError('process_select function is not implemented')
