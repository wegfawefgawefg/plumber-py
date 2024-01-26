from pprint import pprint
from tiles import Tiles


class Stage:
    def __init__(self):
        self.dims = None
        self.entities = []
        self.tiles = None

    def set_tiles(self, tiles):
        self.dims = (len(tiles), len(tiles[0]))
        self.tiles = tiles

    def set_entities(self, entities):
        self.entities = entities

    def get_tile(self, x, y):
        if x < 0 or x >= self.dims[0]:
            return None
        if y < 0 or y >= self.dims[1]:
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


STAGE_ONE.set_tiles(floor(fill_with_air(16, 16), 2))

if __name__ == "__main__":
    pprint(STAGE_ONE.tiles)
