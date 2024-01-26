import copy
from pprint import pprint

import glm
from entity import DisplayState, Entity, EntityType
from sprites.sprite_animator import SpriteAnimator
from sprites.sprite_definitions import PLAYER_STANDING, SpriteFamily
from tiles import TILE_SIZE, Tiles


class Stage:
    def __init__(self):
        self.dims = None
        self.entities = []
        self.tiles = None

    def set_tiles(self, tiles):
        self.dims = glm.vec2(len(tiles[0]), len(tiles))
        self.tiles = tiles

    def set_entities(self, entities):
        self.entities = entities

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

    def get_tile_coord_pairs_in_rect(self, tl, br) -> list:
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
                tile_coord_pairs.append((tile, coord))
        return tile_coord_pairs


STAGE_ONE = Stage()


def fill_with_air(width, height):
    return [[Tiles.AIR for _ in range(width)] for _ in range(height)]


def floor(tiles, height):
    assert height < 16
    h_i = 16 - height
    for h in range(h_i, 16):
        for c, col in enumerate(tiles[h]):
            tiles[h][c] = Tiles.BRICK
    return tiles


def put_a_win_tile(tiles):
    x = len(tiles[0]) - 2
    y = len(tiles) - 3
    tiles[y][x] = Tiles.WIN
    return tiles


t = fill_with_air(64, 16)
t = floor(t, 2)
t = put_a_win_tile(t)
STAGE_ONE.set_tiles(t)

player = Entity()
player.type = EntityType.PLAYER
player.pos = glm.vec2(4 * TILE_SIZE, 2 * TILE_SIZE)
player.size = glm.vec2(TILE_SIZE, TILE_SIZE)
player.vel = glm.vec2(0, 0)
player.acc = glm.vec2(0, 0)
player.input_controlled = (True,)
player.display_state = DisplayState.IDLE
player.sprite_animator = SpriteAnimator(
    SpriteFamily.PLAYER,
    PLAYER_STANDING,
)
# player_2 = copy.deepcopy(player)
# player_2.pos.x += TILE_SIZE * 10

STAGE_ONE.set_entities([player])
# STAGE_ONE.set_entities([player, player_2])


if __name__ == "__main__":
    pprint(STAGE_ONE.tiles)
