import random
from random import randrange, shuffle

from dune_rogue.logic.ai.status_effects.status_effect import StatusEffect
from dune_rogue.logic.entities.acting_entity import CharacterEntity
from dune_rogue.logic.entities.factories.animals import AnimalsFactory
from dune_rogue.logic.entities.factories.factory import EntityFactory
from dune_rogue.logic.entities.factories.machines import MachinesFactory
from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.entities.npcs.npc import Enemy, NPC
from dune_rogue.logic.levels.mediator import LevelMediator
from dune_rogue.render.color import WHITE_COLOR, Color
from dune_rogue.render.scene import Scene
from dune_rogue.logic.actions import Action
from dune_rogue.logic.states import State


_MIN_ROOM_SIZE = 4
_MAX_ROOM_SIZE = 10
_MIN_ROOMS = 5
_MAX_ROOMS = 10
_MAX_ENTITIES = 15
_MIN_ENTITIES = 4
_MAX_ITEMS = 3
_GEN_ITERS = 10


class Level(Scene):
    """Level class"""
    mult = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
    ]

    def __init__(self, load_file, player):
        """
        :param load_file: file to load level from
        :param player: player character entity
        """
        self.w = 0
        self.h = 0
        self.static_entities = []
        self.acting_entities = []
        self.player = player
        self.is_finished = False
        self.finish_coord = None
        self.explored = []
        self.visible = []
        self.light = False

        self._STATIC_ENTITY_MAPPING = {}
        self._ACTING_ENTITY_MAPPING = {}
        self.factory = None

        if load_file:
            self.load_from_file(load_file)

    def render(self):
        self.update_visibility()
        text = list(map(lambda ents: list(map(str, ents)), self.static_entities))
        colors = [[Color(50, 50, 50)] * self.w for _ in range(self.h)]
        solid = [[False] * self.w for _ in range(self.h)]
        for i in range(self.h):
            for j in range(self.w):
                text[i][j] = text[i][j] if self.explored[i][j] else ' '
                if self.visible[i][j]:
                    colors[i][j] = self.static_entities[i][j].glyph.color
                solid[i][j] = self.static_entities[i][j].is_solid

        for ent in self.acting_entities:
            if not solid[ent.y][ent.x]:
                solid[ent.y][ent.x] = ent.is_solid
                if self.visible[ent.y][ent.x]:
                    text[ent.y][ent.x] = ent.glyph.symbol
                    colors[ent.y][ent.x] = ent.glyph.color
        text[self.player.y][self.player.x] = self.player.glyph.symbol
        colors[self.player.y][self.player.x] = self.player.glyph.color

        stats_text = str(self.player.stats)
        return [[text], [[stats_text]]], [[colors], [[[WHITE_COLOR] * len(stats_text)]]]

    def filter_entities(self):
        dead = list(filter(lambda e: not e.is_alive, self.acting_entities))
        for ent in dead:
            if isinstance(ent, Enemy):
                self.player.stats.give_exp(ent.exp)
        self.acting_entities = list(filter(lambda e: e.is_alive, self.acting_entities))

    def process_input(self, action):
        mediator = LevelMediator(self)

        if action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            target_coord = (
                    self.player.x - (action == Action.MOVE_LEFT) + (action == Action.MOVE_RIGHT),
                    self.player.y - (action == Action.MOVE_UP) + (action == Action.MOVE_DOWN)
            )
            intersect_entity = mediator.get_entity_at(target_coord[0], target_coord[1])
            if not intersect_entity.is_solid:
                self.player.x, self.player.y = target_coord
            self.player.intersect(intersect_entity)
        elif action == Action.TOGGLE_PAUSE:
            return State.PAUSE_MENU
        elif action == Action.TOGGLE_INVENTORY:
            return State.INVENTORY
        elif action == Action.PICK_PUT:
            for i, ent in enumerate(self.acting_entities[::-1]):
                if isinstance(ent, ItemEntity) and ent.x == self.player.x and ent.y == self.player.y:
                    self.player.inventory.add_item(ent.item)
                    del self.acting_entities[-i - 1]
                    break

        if not self.player.is_alive:
            return State.MAIN_MENU

        self.filter_entities()
        for i, ent in enumerate(self.acting_entities):
            ent.update(mediator)
            if not self.player.is_alive:
                return State.MAIN_MENU
        self.acting_entities += mediator.new_entities
        self.filter_entities()

        for ent in self.acting_entities:
            if isinstance(ent, CharacterEntity):
                ent.regen()

        for ent in self.acting_entities:
            if isinstance(ent, NPC):
                if isinstance(ent.behavior, StatusEffect):
                    ent.behavior.purify_others()
                    if ent.behavior.duration <= 0:
                        ent.behavior = ent.behavior.behavior

        if self.player.x == self.finish_coord[0] and self.player.y == self.finish_coord[1]:
            self.is_finished = True
        return State.LEVEL

    def set_factory(self, factory):
        self.factory = factory
        self._STATIC_ENTITY_MAPPING = {
            '#': factory.create_wall,
            ' ': factory.create_floor,
            'X': factory.create_finish,
        }

        self._ACTING_ENTITY_MAPPING = {
            'a': factory.create_aggressive,
            'c': factory.create_coward,
            'p': factory.create_passive,
            'r': factory.create_ghola,
            '|': factory.create_unfixed_crys,
            '&': factory.create_worn_stillsuit,
            # '@': EntityFactory.create_player_character
        }

    def load_from_file(self, file_name):
        """Loads level from file
        :argument file_name: file to load from
        """
        with open(file_name, 'r') as file:
            factory_type = file.readline().strip()

            if factory_type == 'animals':
                self.set_factory(AnimalsFactory())
            elif factory_type == 'machines':
                self.set_factory(MachinesFactory())
            else:
                raise ValueError(f'Unknown level type {factory_type}')

            w, h = map(int, file.readline().split())
            self.w, self.h = w, h
            self.static_entities = []
            self.acting_entities = []

            for i in range(h):
                ent_row = []
                ent_symbols = file.readline()
                for j in range(w):
                    ent_row.append(self._STATIC_ENTITY_MAPPING[ent_symbols[j]](j, i))
                    if ent_symbols[j] == 'X':
                        self.finish_coord = (j, i)
                self.static_entities.append(ent_row)
                self.explored.append([False] * w)


            n_acting = int(file.readline())

            for _ in range(n_acting):
                ent_symbol, x, y = file.readline().split()
                x, y = int(x), int(y)
                if ent_symbol == '@':
                    self.player.x = x
                    self.player.y = y
                    self.acting_entities.append(self.player)
                else:
                    self.acting_entities.append(self._ACTING_ENTITY_MAPPING[ent_symbol](x, y))

    class Room:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def generate(self, w, h, factory):
        """Generates random level
        :argument w: width
        :argument h: height
        :argument factory: entities factory
        """
        self.set_factory(factory)

        self.static_entities = [['#'] * w for _ in range(h)]
        self.acting_entities = []
        self.w = w
        self.h = h
        rooms = []
        self.explored = [[False] * w for _ in range(h)]

        total_rooms = randrange(_MIN_ROOMS, _MAX_ROOMS)
        for i in range(_GEN_ITERS):
            for r in range(total_rooms):
                if len(rooms) >= _MAX_ROOMS:
                    break

                width = randrange(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
                height = randrange(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
                if w - width - 1 < 2 or h - height - 1 < 2:
                    continue
                x = randrange(1, w - width - 1)
                y = randrange(1, h - height - 1)

                room = self.Room(x, y, width, height)

                def check_overlap(room, rooms):
                    for other in rooms:
                        if (room.x <= other.x + other.w and room.x + room.w >= other.x) and\
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
                    self.static_entities[y][x] = ' '

        shuffle(rooms)
        for i in range(len(rooms) - 1):
            r1 = rooms[i]
            r2 = rooms[i + 1]

            for x in range(r1.x, r2.x + 1):
                self.static_entities[r1.y][x] = ' '
            for y in range(r1.y, r2.y + 1):
                self.static_entities[y][r1.x] = ' '
            for x in range(r2.x, r1.x + 1):
                self.static_entities[r1.y][x] = ' '
            for y in range(r2.y, r1.y + 1):
                self.static_entities[y][r1.x] = ' '
            for x in range(r1.x, r2.x + 1):
                self.static_entities[r2.y][x] = ' '
            for y in range(r1.y, r2.y + 1):
                self.static_entities[y][r2.x] = ' '
            for x in range(r2.x, r1.x + 1):
                self.static_entities[r2.y][x] = ' '
            for y in range(r2.y, r1.y + 1):
                self.static_entities[y][r2.x] = ' '

        for i in range(h):
            for j in range(w):
                self.static_entities[i][j] = self._STATIC_ENTITY_MAPPING[self.static_entities[i][j]](j, i)

        def get_random_pos():
            rnd_room = rooms[randrange(0, len(rooms))]
            x_pos = randrange(0, rnd_room.w) + rnd_room.x
            y_pos = randrange(0, rnd_room.h) + rnd_room.y
            return x_pos, y_pos

        finish_x_pos, finish_y_pos = get_random_pos()
        self.finish_coord = (finish_x_pos, finish_y_pos)
        self.static_entities[finish_y_pos][finish_x_pos] = self._STATIC_ENTITY_MAPPING['X'](finish_y_pos, finish_x_pos)

        x_pos, y_pos = get_random_pos()
        while x_pos == finish_x_pos and y_pos == finish_y_pos:
            x_pos, y_pos = get_random_pos()

        self.player.x = x_pos
        self.player.y = y_pos
        self.acting_entities.append(self.player)

        mediator = LevelMediator(self)
        n_entities = randrange(_MIN_ENTITIES, _MAX_ENTITIES)
        n_items = 0

        for _ in range(_GEN_ITERS):
            for _ in range(n_entities):
                if len(self.acting_entities) >= n_entities + 1:
                    break

                x_pos, y_pos = get_random_pos()
                old_ent = mediator.get_entity_at(x_pos, y_pos)
                if old_ent.is_solid:
                    continue

                symb = random.choice(list(self._ACTING_ENTITY_MAPPING.keys()))
                ent = self._ACTING_ENTITY_MAPPING[symb](x_pos, y_pos)
                if symb == 'r':
                    for i in range(randrange(2, 4)):
                        for j in range(randrange(2, 4)):
                            for dx in range(-i, i + 1):
                                for dy in range(-j, j + 1):
                                    ex = x_pos + dx
                                    ey = y_pos + dy
                                    if ex >= self.w or ey >= self.h or self.static_entities[ey][ex].is_solid or random.random() < 0.5:
                                        continue
                                    c_ent = self._ACTING_ENTITY_MAPPING[symb](ex, ey)
                                    self.acting_entities.append(c_ent)
                                    n_entities += 1
                if isinstance(ent, ItemEntity):
                    if n_items >= _MAX_ITEMS:
                        continue
                    n_items += 1
                self.acting_entities.append(ent)

    ### Lighting code is from here http://www.roguebasin.com/index.php/Python_shadowcasting_implementation
    def blocked(self, x, y):
        return (x < 0 or y < 0
                or x >= self.w or y >= self.h
                or self.static_entities[y][x].is_solid)

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        "Recursive lightcasting function"
        if start < end:
            return
        radius_squared = radius * radius
        for j in range(row, radius + 1):
            dx, dy = -j - 1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.visible[Y][X] = True
                        self.explored[Y][X] = True
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def do_fov(self, x, y, radius):
        "Calculate lit squares from the given location and radius"
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct], 0)

    def update_visibility(self, r=6):
        if self.light:
            self.visible = []
            self.visible = [[False] * self.w for _ in range(self.h)]

            x_orig = self.player.x
            y_orig = self.player.y

            self.do_fov(x_orig, y_orig, r)
        else:
            self.visible = [[True] * self.w for _ in range(self.h)]
            self.explored = self.visible

    def __str__(self):
        field = list(map(lambda ents: ''.join(map(str, ents)), self.static_entities))
        for ent in self.acting_entities:
            field[ent.y][ent.x] = ent.glyph.symbol
        return '\n'.join(field)
