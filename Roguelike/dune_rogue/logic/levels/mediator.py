class LevelMediator:
    """Provides access to level for entity"""
    def __init__(self, level):
        """
        :param level: level reference
        """
        self.level = level

    def get_level_shape(self):
        """Returns level shape
        :return: level shape
        """
        return self.level.w, self.level.h

    def get_all_entities(self):
        """Returns all entities
        :return: all static and acting entities at the level
        """
        return self.level.static_entities, self.level.acting_entities

    def get_entity_at(self, x, y):
        """Returns entity at given coordinates
        :param x: x coordinate
        :param y: y coordinate
        :return:
        """
        for ent in self.level.acting_entities:
            if ent.x == x and ent.y == y:
                return ent
        return self.level.static_entities[y][x]
