class LevelMediator:
    """Provides access to level for entity"""
    def __init__(self, level):
        """
        :param level: level reference
        """
        self.level = level
        self.new_entities = []
        self.new_coords = [[False] * level.w for _ in range(level.h)]

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
        if not self.inside_level(coord):
            return None
        for ent in self.level.acting_entities:
            if ent.coord == coord:
                return ent
        return self.level.static_entities[coord.y][coord.x]

    def add_entity(self, entity):
        """Add new entity to the level
        :param entity: entity to add
        """
        self.new_entities.append(entity)
        self.new_coords[entity.y][entity.x] = True

    def inside_level(self, coord):
        """Checks if coordinate is inside level
        :param coord: coordinate
        :return: whether inside level or not
        """
        return self.level.w > coord.x >= 0 and self.level.h > coord.y >= 0
