class Inventory:
    """Inventory class"""
    def __check(self):
        """Checks whether inventory is valid"""
        if self.weight > self.capacity:
            raise RuntimeError('Inventory is overloaded')

    def __init__(self, capacity, items=None):
        """
        :param capacity: maximum capacity that can be carried
        :param items: list of carried items
        """
        self.weight = 0
        self.capacity = capacity
        if items is None:
            self.items = []
        else:
            self.items = items
            for item in items:
                self.weight += item.weight
        self.__check()

    def can_take(self, weight):
        """Checks whether provided weight can be carried
        :argument weight: weight to check
        :return: True if weight can be taken. False otherwise
        """
        return self.weight + weight <= self.capacity

    def add_item(self, item):
        """Adds an item to the inventory
        :argument item: item to be added
        """
        self.weight += item.weight
        try:
            self.__check()
        except RuntimeError as e:
            self.weight -= item.weight
            raise e
        self.items.append(item)

    def remove_item(self, item_id):
        """Removes item from the inventory
        :param item_id: item id in the inventory
        """
        self.weight -= self.items[item_id].weight
        try:
            self.__check()
        except RuntimeError as e:
            self.weight += self.items[item_id].weight
            raise e
        del self.items[item_id]
