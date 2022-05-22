import os
from abc import ABC
from pathlib import Path
import random
from random import randrange, shuffle

from dune_rogue.logic.coordinate import Coordinate
from dune_rogue.logic.entities.factories.animals import AnimalsFactory
from dune_rogue.logic.entities.factories.machines import MachinesFactory
from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.levels.level import Level
from dune_rogue.logic.levels.mediator import LevelMediator

_MIN_ROOM_SIZE = 4
_MAX_ROOM_SIZE = 10
_MIN_ROOMS = 5
_MAX_ROOMS = 10
_MAX_ENTITIES = 15
_MIN_ENTITIES = 4
_MAX_ITEMS = 3
_GEN_ITERS = 10


class LevelBuilder(ABC):
    def __init__(self):
        self.factory = None

    """Abstract level builder class"""
    def set_sizes(self, w, h):
        """Set level sized before build"""
        pass

    def build(self, player):
        """Builds level"""
        raise NotImplementedError('build is not implemented')

    def reset(self):
        """Resets builder"""
        pass

    def set_factory(self, factory):
        """Sets factory for levels building"""
        self.factory = factory


class LevelLoader(LevelBuilder):
    """Loader for levels"""
    def __init__(self):
        super().__init__()
        cwd = os.path.realpath(__file__)
        path = Path(cwd)
        self.levels_dir = str(path.parent.absolute()) + os.sep + 'predefined' + os.sep
        self.current_level = 0
        self.number_of_levels = len(os.listdir(self.levels_dir))
        self.level = None

    def build(self, player):
        """ Loads next level from file
        :argument player: player character
        :return: next level
        """
        self.current_level += 1
        if self.current_level > self.number_of_levels:
            return None
        self.load_from_file(self.levels_dir + f'level_{self.current_level}.lvl', player)
        return self.level

    def reset(self):
        """Start loading levels from the first"""
        self.current_level = 0

    def load_from_file(self, file_name, player):
        """Loads level from file
        :argument file_name: file to load from
        :argument player: player reference
        :returns: new level
        """
        self.level = Level(player)
        with open(file_name, 'r') as file:
            factory_type = file.readline().strip()

            if factory_type == 'animals':
                self.level.set_factory(AnimalsFactory())
            elif factory_type == 'machines':
                self.level.set_factory(MachinesFactory())
            else:
                raise ValueError(f'Unknown level type {factory_type}')

            w, h = map(int, file.readline().split())
            self.level.w, self.level.h = w, h
            self.level.static_entities = []
            self.level.acting_entities = []

            for i in range(h):
                ent_row = []
                ent_symbols = file.readline()
                for j in range(w):
                    ent_row.append(self.level.static_entity_mapping[ent_symbols[j]](j, i))
                    if ent_symbols[j] == 'X':
                        self.level.finish_coord = Coordinate(j, i)
                self.level.static_entities.append(ent_row)
                self.level.explored.append([False] * w)

            n_acting = int(file.readline())

            for _ in range(n_acting):
                ent_symbol, x, y = file.readline().split()
                x, y = int(x), int(y)
                if ent_symbol == '@':
                    self.level.player.x = x
                    self.level.player.y = y
                    self.level.acting_entities.append(self.level.player)
                else:
                    self.level.acting_entities.append(self.level.acting_entity_mapping[ent_symbol](x, y))
        return self.level


class LevelGenerator(LevelBuilder):
    """Generator for levels"""
    def __init__(self):
        super().__init__()
        self.w = None
        self.h = None
        self.level = None

    def build(self, player):
        """ Generates random level
        :argument player: player character
        :return: next level
        """
        if not self.w or not self.h:
            raise ValueError('width and height must be set before generating level')

        self.generate(self.w, self.h, self.factory, player)

        self.w = None
        self.h = None

        return self.level

    class Room:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def generate_rooms(self):
        rooms = []
        total_rooms = randrange(_MIN_ROOMS, _MAX_ROOMS)
        for i in range(_GEN_ITERS):
            for r in range(total_rooms):
                if len(rooms) >= _MAX_ROOMS:
                    break

                width = randrange(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
                height = randrange(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
                if self.level.w - width - 1 < 2 or self.level.h - height - 1 < 2:
                    continue
                x = randrange(1, self.level.w - width - 1)
                y = randrange(1, self.level.h - height - 1)

                room = self.Room(x, y, width, height)

                def check_overlap(room, rooms):
                    for other in rooms:
                        if (room.x <= other.x + other.w and room.x + room.w >= other.x) and \
                                (room.y <= other.y + other.h and room.y + room.h >= other.y):
                            return True
                    return False

                if check_overlap(room, rooms):
                    pass
                else:
                    rooms.append(room)
        for room in rooms:
            for y in range(room.y, room.y + room.h):
                for x in range(room.x, room.x + room.w):
                    self.level.static_entities[y][x] = ' '
        shuffle(rooms)
        return rooms

    def generate_corridors(self, rooms):
        for i in range(len(rooms) - 1):
            r1 = rooms[i]
            r2 = rooms[i + 1]

            for x in range(r1.x, r2.x + 1):
                self.level.static_entities[r1.y][x] = ' '
            for y in range(r1.y, r2.y + 1):
                self.level.static_entities[y][r1.x] = ' '
            for x in range(r2.x, r1.x + 1):
                self.level.static_entities[r1.y][x] = ' '
            for y in range(r2.y, r1.y + 1):
                self.level.static_entities[y][r1.x] = ' '
            for x in range(r1.x, r2.x + 1):
                self.level.static_entities[r2.y][x] = ' '
            for y in range(r1.y, r2.y + 1):
                self.level.static_entities[y][r2.x] = ' '
            for x in range(r2.x, r1.x + 1):
                self.level.static_entities[r2.y][x] = ' '
            for y in range(r2.y, r1.y + 1):
                self.level.static_entities[y][r2.x] = ' '

    @staticmethod
    def get_random_pos(rooms):
        rnd_room = rooms[randrange(0, len(rooms))]
        return Coordinate(randrange(0, rnd_room.w) + rnd_room.x, randrange(0, rnd_room.h) + rnd_room.y)

    def generate_acting_entities(self, rooms):
        mediator = LevelMediator(self.level)
        n_entities = randrange(_MIN_ENTITIES, _MAX_ENTITIES)
        n_items = 0

        for _ in range(_GEN_ITERS):
            for _ in range(n_entities):
                if len(self.level.acting_entities) >= n_entities + 1:
                    break

                pos = self.get_random_pos(rooms)
                old_ent = mediator.get_entity_at(pos)
                if old_ent.is_solid:
                    continue

                symb = random.choice(list(self.level.acting_entity_mapping.keys()))
                ent = self.level.acting_entity_mapping[symb](pos.x, pos.y)
                if symb == 'r':
                    for i in range(randrange(2, 4)):
                        for j in range(randrange(2, 4)):
                            for dx in range(-i, i + 1):
                                for dy in range(-j, j + 1):
                                    e_pos = pos + Coordinate(dx, dy)
                                    if not mediator.inside_level(e_pos) or self.level.static_entities[e_pos.y][e_pos.x].is_solid or random.random() < 0.5:
                                        continue
                                    c_ent = self.level.acting_entity_mapping[symb](e_pos.x, e_pos.y)
                                    self.level.acting_entities.append(c_ent)
                                    n_entities += 1

                if isinstance(ent, ItemEntity):
                    if n_items >= _MAX_ITEMS:
                        continue
                    n_items += 1
                self.level.acting_entities.append(ent)

    def put_entities(self, rooms):
        for i in range(self.h):
            for j in range(self.w):
                self.level.static_entities[i][j] = self.level.static_entity_mapping[self.level.static_entities[i][j]](j, i)

        finish_pos = self.get_random_pos(rooms)
        self.level.finish_coord = finish_pos
        self.level.static_entities[finish_pos.y][finish_pos.x] = self.level.static_entity_mapping['X'](finish_pos.x, finish_pos.y)

        pos = self.get_random_pos(rooms)
        while pos == finish_pos:
            pos = self.get_random_pos(rooms)

        self.level.player.coord = pos
        self.level.acting_entities.append(self.level.player)

        self.generate_acting_entities(rooms)

    def generate(self, w, h, factory, player):
        """Generates random level
        :argument w: width
        :argument h: height
        :argument factory: entities factory
        :argument player: player reference
        :returns: new level
        """
        self.level = Level(player)
        self.level.set_factory(factory)

        self.level.static_entities = [['#'] * w for _ in range(h)]
        self.level.acting_entities = []
        self.level.w = w
        self.level.h = h

        self.level.explored = [[False] * w for _ in range(h)]

        rooms = self.generate_rooms()
        self.generate_corridors(rooms)
        self.put_entities(rooms)

        return self.level

    def set_sizes(self, w, h):
        if w <= 0 or h <= 0:
            raise ValueError('width and height must be positive')
        # + 1 because of edges
        self.w = int(w) + 1
        self.h = int(h) + 1
