import random
from random import randrange, shuffle

from dune_rogue.logic.ai.status_effects.status_effect import StatusEffect
from dune_rogue.logic.entities.factories.animals import AnimalsFactory
from dune_rogue.logic.entities.factories.machines import MachinesFactory
from dune_rogue.logic.coordinate import Coordinate
from dune_rogue.logic.entities.items.item_entity import ItemEntity
from dune_rogue.logic.entities.npcs.npc import Enemy, NPC
from dune_rogue.logic.levels.mediator import LevelMediator
from dune_rogue.render.color import WHITE_COLOR, Color, GREY_COLOR
from dune_rogue.render.scene import Scene
from dune_rogue.logic.actions import Action
from dune_rogue.logic.states import State


class Level(Scene):
    """Level class"""
    # Matrix for lighting, see http://www.roguebasin.com/index.php/Python_shadowcasting_implementation
    mult = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
    ]

    def __init__(self, player):
        """
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

        self.static_entity_mapping = {}
        self.acting_entity_mapping = {}
        self.factory = None

    def render(self):
        self.update_visibility()
        text = list(map(lambda ents: list(map(str, ents)), self.static_entities))
        colors = [[GREY_COLOR] * self.w for _ in range(self.h)]
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

    def process_move(self, action, mediator):
        target_coord = Coordinate(
            self.player.x - (action == Action.MOVE_LEFT) + (action == Action.MOVE_RIGHT),
            self.player.y - (action == Action.MOVE_UP) + (action == Action.MOVE_DOWN)
        )
        intersect_entity = mediator.get_entity_at(target_coord)
        if not intersect_entity.is_solid:
            self.player.coord = target_coord
        self.player.intersect(intersect_entity)

    def process_pick(self):
        for i, ent in enumerate(self.acting_entities[::-1]):
            if isinstance(ent, ItemEntity) and ent.x == self.player.x and ent.y == self.player.y:
                self.player.inventory.add_item(ent.item)
                del self.acting_entities[-i - 1]
                break

    def update_entities(self, mediator):
        self.filter_entities()
        for i, ent in enumerate(self.acting_entities):
            ent.update(mediator)
            if not self.player.is_alive:
                return State.MAIN_MENU
        self.acting_entities += mediator.new_entities
        self.filter_entities()

    def update_status_effects(self):
        for ent in self.acting_entities:
            if isinstance(ent, NPC) and isinstance(ent.behavior, StatusEffect):
                ent.behavior.purify_others()
                if ent.behavior.duration <= 0:
                    ent.behavior = ent.behavior.behavior

    def process_input(self, action):
        mediator = LevelMediator(self)

        if action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            self.process_move(action, mediator)
        elif action == Action.TOGGLE_PAUSE:
            return State.PAUSE_MENU
        elif action == Action.TOGGLE_INVENTORY:
            return State.INVENTORY
        elif action == Action.PICK_PUT:
            self.process_pick()

        if not self.player.is_alive:
            return State.MAIN_MENU

        self.update_entities(mediator)
        self.update_status_effects()

        if self.player.coord == self.finish_coord:
            self.is_finished = True
        return State.LEVEL

    def set_factory(self, factory):
        self.factory = factory
        self.static_entity_mapping = {
            '#': factory.create_wall,
            ' ': factory.create_floor,
            'X': factory.create_finish,
        }

        self.acting_entity_mapping = {
            'a': factory.create_aggressive,
            'c': factory.create_coward,
            'p': factory.create_passive,
            'r': factory.create_ghola,
            '|': factory.create_unfixed_crys,
            '&': factory.create_worn_stillsuit,
            # '@': EntityFactory.create_player_character
        }

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
