from pprint import pprint

import glm
from tiles import Tiles


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

if __name__ == "__main__":
    pprint(STAGE_ONE.tiles)
