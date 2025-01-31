import copy
from enum import Enum, auto
from pprint import pprint
import random

import glm
from entity import DisplayState, Entity, EntityType
from entity_templates import player_template
from sprites.sprite_animator import SpriteAnimator
from sprites.sprite_definitions import PLAYER_STANDING, SpriteFamily
from tiles import TILE_SIZE, Tile


class TileCoordPair:
    def __init__(self, tile, coord):
        self.tile = tile
        self.coord = coord


class Exit:
    def __init__(self, goes_to, level_win=False):
        self.goes_to = goes_to
        self.level_win = level_win


class Decoration:
    def __init__(self, pos, sprite_animator, flip=False):
        self.pos = pos
        self.sprite_animator = sprite_animator
        self.flip = flip

    def step(self):
        self.sprite_animator.step()


class SpecialDecoration(Decoration):
    def __init__(self, pos, sprite_animator, flip=False):
        super().__init__(pos, sprite_animator, flip)
        self.active = False

    def step(self):
        if self.active:
            self.sprite_animator.step()


class Stage:
    def __init__(self):
        self.won = False
        self.entities = []
        self.exits = {}
        self.tiles = None

        self.foreground_decorations = []
        self.background_decorations = []
        self.special_decorations = []

    @property
    def dims(self):
        """Returns the dimensions of the stage in tile coordinates"""
        return glm.vec2(len(self.tiles[0]), len(self.tiles))

    @property
    def wc_dims(self):
        """Returns the dimensions of the stage in world coordinates"""
        return self.dims * TILE_SIZE

    def add_foreground_decoration(self, decoration):
        self.foreground_decorations.append(decoration)

    def add_background_decoration(self, decoration):
        self.background_decorations.append(decoration)

    def add_special_decoration(self, decoration):
        self.special_decorations.append(decoration)

    def set_tiles(self, tiles):
        self.tiles = tiles

    def add_exit(self, pos, goes_to, level_win=False):
        print(self.dims)
        # make sure pos in range
        if pos.x < 0 or pos.x >= self.dims.x or pos.y < 0 or pos.y >= self.dims.y:
            raise Exception("win tile pos out of the stage!!!")
        self.tiles[pos.y][pos.x] = Tile.EXIT
        self.exits[pos.to_tuple()] = Exit(goes_to, level_win)

    def get_exit(self, pos):
        return self.exits.get(pos.as_tuple())

    def set_entities(self, entities):
        self.entities = entities

    def get_height(self):
        """Returns the height of the stage in world coordinates"""
        return self.wc_dims.y

    def get_width(self):
        """Returns the width of the stage in world coordinates"""
        return self.wc_dims.x

    def get_tile(self, x, y):
        if x < 0 or x >= self.dims.x:
            return None
        if y < 0 or y >= self.dims.y:
            return None
        return self.tiles[y][x]

    def get_tiles_in_rect(self, tl, br) -> list:
        # /** returns all the tiles in a given search rectangle: defined by top_left and bottom_right positions
        # * search rectangle is inclusive and should be in tile coordinates
        # * cannot fail. coords are clamped to stage boundaries. a search rectangle that is completely outside the stage will return an empty vector
        # */

        # if search rect is completely outside the stage, return an empty vector
        #  dont need to check less than zero, (top left corner case) because unsigned ints cant be negative
        if tl.x > self.dims.x or tl.y > self.dims.y:
            return []

        # in case search rect partially outside stage, clamp coords
        tl = glm.ivec2(
            max(0, tl.x),
            max(0, tl.y),
        )
        br = glm.ivec2(
            min(self.dims.x, br.x),
            min(self.dims.y, br.y),
        )

        tiles = []
        for y in range(tl.y, br.y + 1):
            for x in range(tl.x, br.x + 1):
                tiles.append(self.get_tile(x, y))
        return tiles

    def get_tile_coord_pairs_in_rect(self, tl, br) -> list[TileCoordPair]:
        # /** just like get_tiles_in_rect, but also returns coords */
        # if search rect is completely outside the stage, return an empty vector
        if tl.x > self.dims.x or tl.y > self.dims.y:
            return []

        # in case search rect partially outside stage, clamp coords
        tl = glm.ivec2(
            max(0, tl.x),
            max(0, tl.y),
        )
        br = glm.ivec2(
            min(self.dims.x, br.x),
            min(self.dims.y, br.y),
        )

        tile_coord_pairs = []
        for y in range(tl.y, br.y + 1):
            for x in range(tl.x, br.x + 1):
                tile = self.get_tile(x, y)
                coord = glm.uvec2(x, y)
                tile_coord_pairs.append(TileCoordPair(tile, coord))
        return tile_coord_pairs
