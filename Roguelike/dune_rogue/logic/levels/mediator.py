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

    def get_entity_at(self, coord):
        """Returns entity at given coordinates
        :param coord: coordinate
        :return:
        """
        for ent in self.level.acting_entities:
            if ent.coord == coord:
                return ent
        return self.level.static_entities[coord.y][coord.x]

    def inside_level(self, coord):
        """Checks if coordinate is inside level
        :param coord: coordinate
        :return: whether inside level or not
        """
        return self.level.w > coord.x >= 0 and self.level.h > coord.y >= 0
