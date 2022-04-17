import os
import random
from pathlib import Path
from random import randrange, shuffle

from dune_rogue.logic.ai.status_effects.status_effect import StatusEffect
from dune_rogue.logic.entities.factory import EntityFactory
from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.entities.npcs.npc import Enemy, NPC
from dune_rogue.logic.levels.mediator import LevelMediator
from dune_rogue.render.color import WHITE_COLOR
from dune_rogue.render.scene import Scene
from dune_rogue.logic.actions import Action
from dune_rogue.logic.states import State

_STATIC_ENTITY_MAPPING = {
    '#': EntityFactory.create_wall,
    ' ': EntityFactory.create_floor,
    'X': EntityFactory.create_finish,
}

_ACTING_ENTITY_MAPPING = {
    'c': EntityFactory.create_cielago,
    'm': EntityFactory.create_mouse,
    'f': EntityFactory.create_fox,
    '|': EntityFactory.create_unfixed_crys,
    '&': EntityFactory.create_worn_stillsuit,
    # '@': EntityFactory.create_player_character
}

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
    def render(self):
        text = list(map(lambda ents: list(map(str, ents)), self.static_entities))
        colors = [[WHITE_COLOR] * self.w for _ in range(self.h)]
        solid = [[False] * self.w for _ in range(self.h)]
        for i in range(self.h):
            for j in range(self.w):
                colors[i][j] = self.static_entities[i][j].glyph.color
                solid[i][j] = self.static_entities[i][j].is_solid

        for ent in self.acting_entities:
            if not solid[ent.y][ent.x]:
                solid[ent.y][ent.x] = ent.is_solid
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
        self.filter_entities()

        for ent in self.acting_entities:
            if isinstance(ent, NPC):
                if isinstance(ent.behavior, StatusEffect):
                    ent.behavior.purify_others()
                    if ent.behavior.duration <= 0:
                        ent.behavior = ent.behavior.behavior

        if self.player.x == self.finish_coord[0] and self.player.y == self.finish_coord[1]:
            self.is_finished = True
        return State.LEVEL

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
        if load_file:
            self.load_from_file(load_file)

    def load_from_file(self, file_name):
        """Loads level from file
        :argument file_name: file to load from
        """
        with open(file_name, 'r') as file:
            w, h = map(int, file.readline().split())
            self.w, self.h = w, h
            self.static_entities = []
            self.acting_entities = []

            for i in range(h):
                ent_row = []
                ent_symbols = file.readline()
                for j in range(w):
                    ent_row.append(_STATIC_ENTITY_MAPPING[ent_symbols[j]](j, i))
                    if ent_symbols[j] == 'X':
                        self.finish_coord = (j, i)
                self.static_entities.append(ent_row)
            n_acting = int(file.readline())

            for _ in range(n_acting):
                ent_symbol, x, y = file.readline().split()
                x, y = int(x), int(y)
                if ent_symbol == '@':
                    self.player.x = x
                    self.player.y = y
                    self.acting_entities.append(self.player)
                else:
                    self.acting_entities.append(_ACTING_ENTITY_MAPPING[ent_symbol](x, y))

    class Room:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def generate(self, w, h):
        """Generates random level
        :argument w: width
        :argument h: height
        """
        self.static_entities = [['#'] * w for _ in range(h)]
        self.acting_entities = []
        self.w = w
        self.h = h
        rooms = []

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
                self.static_entities[i][j] = _STATIC_ENTITY_MAPPING[self.static_entities[i][j]](j, i)

        def get_random_pos():
            rnd_room = rooms[randrange(0, len(rooms))]
            x_pos = randrange(0, rnd_room.w) + rnd_room.x
            y_pos = randrange(0, rnd_room.h) + rnd_room.y
            return x_pos, y_pos

        finish_x_pos, finish_y_pos = get_random_pos()
        self.finish_coord = (finish_x_pos, finish_y_pos)
        self.static_entities[finish_y_pos][finish_x_pos] = _STATIC_ENTITY_MAPPING['X'](finish_y_pos, finish_x_pos)

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

                ent = _ACTING_ENTITY_MAPPING[random.choice(list(_ACTING_ENTITY_MAPPING.keys()))](x_pos, y_pos)
                if isinstance(ent, ItemEntity):
                    if n_items >= _MAX_ITEMS:
                        continue
                    n_items += 1
                self.acting_entities.append(ent)

    def __str__(self):
        field = list(map(lambda ents: ''.join(map(str, ents)), self.static_entities))
        for ent in self.acting_entities:
            field[ent.y][ent.x] = ent.glyph.symbol
        return '\n'.join(field)
