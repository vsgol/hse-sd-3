class InventoryItem:
    """Inventory item"""
    def __init__(self, weight=0, usable=False, can_be_equipped=False, stats=None, name="Default name",
                 description='Default description', is_equipped=False):
        """
        :param weight: weight of the item
        :param usable: flag whether item can be used
        :param can_be_equipped: flag whether item can be equipped
        :param stats: item statistics effect
        :param name: item textual name
        :param description: item textual description
        :param is_equipped: flag whether item is currently equipped
        """
        self.weight = weight
        self.can_be_equipped = can_be_equipped
        self.usable = usable
        self.stats = stats
        self.name = name
        self.description = description
        self.is_equipped = is_equipped

    def get_bonuses(self):
        """ Get item stats effect
        :return: statistics bonuses
        """
        return self.stats

    def equip(self):
        """Make item equipped"""
        self.is_equipped = True

    def unequip(self):
        """Make item unequipped"""
        self.is_equipped = False
