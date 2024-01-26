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
player_2 = copy.deepcopy(player)
player_2.pos.x += TILE_SIZE * 10

STAGE_ONE.set_entities([player, player_2])


if __name__ == "__main__":
    pprint(STAGE_ONE.tiles)
