class InventoryItem:
    """Inventory item"""
    def __init__(self, weight=0, usable=False, can_be_equipped=False, stats=None, name="Default name",
                 description='Default description', is_equipped=False, item_type=None):
        """
        :param weight: weight of the item
        :param usable: flag whether item can be used
        :param can_be_equipped: flag whether item can be equipped
        :param stats: item statistics effect
        :param name: item textual name
        :param description: item textual description
        :param is_equipped: flag whether item is currently equipped
        :param item_type: type of the item (e.g. armor or weapon)
        """
        self.weight = weight
        self.can_be_equipped = can_be_equipped
        self.usable = usable
        self.stats = stats
        self.name = name
        self.description = description
        self.is_equipped = is_equipped
        self.item_type = item_type

    def get_bonuses(self):
        """ Get item stats effect
        :return: statistics bonuses
        """
        return self.stats

    def equip(self):
        """Make item equipped"""
        if not self.can_be_equipped:
            raise RuntimeError('Equipping which can\'t be equipped')
        if self.is_equipped:
            raise RuntimeError('Equipping equipped item')
        self.is_equipped = True

    def unequip(self):
        """Make item unequipped"""
        if not self.is_equipped:
            raise RuntimeError('Unequipping unequipped item')
        self.is_equipped = False

    def get_bonuses_str(self):
        bonuses = []

        for name, bonus in [
            ('HP: ', self.stats.hp),
            ('DEF: ', self.stats.defence),
            ('ATK: ', self.stats.attack),
            ('MAX_HP: ', self.stats.max_hp),
        ]:
            if bonus != 0:
                if bonus > 0:
                    name += f'+{bonus}'
                else:
                    name += f'{bonus}'
                bonuses.append(name)
        return ' '.join(bonuses)
