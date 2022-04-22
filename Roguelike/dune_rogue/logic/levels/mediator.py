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

    def get_entity_at(self, x, y):
        """Returns entity at given coordinates
        :param x: x coordinate
        :param y: y coordinate
        :return:
        """
        if not (0 <= x < self.level.w) or not (0 <= y < self.level.h):
            return None
        for ent in self.level.acting_entities:
            if ent.x == x and ent.y == y:
                return ent
        return self.level.static_entities[y][x]

    def add_entity(self, entity):
        """Add new entity to the level
        :param entity: entity to add
        """
        self.new_entities.append(entity)
        self.new_coords[entity.y][entity.x] = True
