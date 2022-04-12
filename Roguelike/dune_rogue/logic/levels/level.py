import os
from pathlib import Path

from dune_rogue.logic.entities.factory import EntityFactory
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
    # '@': EntityFactory.create_player_character
}


class Level(Scene):
    """Level class"""
    def render(self):
        text = list(map(lambda ents: list(map(str, ents)), self.static_entities))
        colors = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.static_entities[i][j].glyph.color)
            colors.append(row)
        for ent in self.acting_entities:
            text[ent.y][ent.x] = ent.glyph.symbol
            colors[ent.y][ent.x] = ent.glyph.color
        text[self.player.y][self.player.x] = self.player.glyph.symbol

        stats_text = str(self.player.stats)
        return [[text], [[stats_text]]], [[colors], [[[WHITE_COLOR] * len(stats_text)]]]

    def process_input(self, action):
        mediator = LevelMediator(self)

        if action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            target_coord = (
                    self.player.x - (action == Action.MOVE_LEFT) + (action == Action.MOVE_RIGHT),
                    self.player.y - (action == Action.MOVE_UP) + (action == Action.MOVE_DOWN)
            )
            if not mediator.get_entity_at(target_coord[0], target_coord[1]).is_solid:
                self.player.x, self.player.y = target_coord
        elif action == Action.TOGGLE_PAUSE:
            return State.PAUSE_MENU
        for ent in self.acting_entities:
            ent.update(mediator)
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

    def __str__(self):
        field = list(map(lambda ents: ''.join(map(str, ents)), self.static_entities))
        for ent in self.acting_entities:
            field[ent.y][ent.x] = ent.glyph.symbol
        return '\n'.join(field)
