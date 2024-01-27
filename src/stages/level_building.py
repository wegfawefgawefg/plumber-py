from enum import Enum, auto
import random
from stage import Exit
from stages.stages import Stages
from tiles import Tile


class ForegroundOrBackground(Enum):
    FOREGROUND = auto()
    BACKGROUND = auto()


def foreground_or_background():
    if random.random() < 0.5:
        return ForegroundOrBackground.FOREGROUND
    return ForegroundOrBackground.BACKGROUND


def blit_tiles(source: [[Tile]], destination: [[Tile]], pos):
    for y, row in enumerate(source):
        for x, col in enumerate(row):
            dx = y + pos.y
            dy = x + pos.x
            # skip if dx dy not in destination size
            if dx < 0 or dx >= len(destination):
                continue
            if dy < 0 or dy >= len(destination[0]):
                continue
            destination[y + pos.y][x + pos.x] = col


def air(width):
    """Returns a list of lists of air tiles with the given width, fixed height of 10"""
    return [[Tile.AIR for _ in range(width)] for _ in range(10)]


def fill_area_with(tiles, tl, br, tile):
    for y in range(tl.y, br.y):
        for x in range(tl.x, br.x):
            # skip if dx dy not in destination size
            if x < 0 or x >= len(tiles):
                continue
            if y < 0 or y >= len(tiles[0]):
                continue
            tiles[y][x] = tile
    return tiles


def floor(tiles, height, cap_tile, tile):
    cieling_height = len(tiles)
    h_i = cieling_height - height
    for h in range(h_i, 10):
        for c, col in enumerate(tiles[h]):
            if h == h_i:
                tiles[h][c] = cap_tile
            else:
                tiles[h][c] = tile
    return tiles


def random_bumps(tiles, height, tile, chance):
    # all the way across, a chance to put a block
    for c in range(len(tiles[0])):
        if random.random() < chance:
            tiles[height][c] = tile
    return tiles


_tile_key_ = {
    "a": Tile.AIR,
    "b": Tile.DIRT,
    "c": Tile.CAPPED_DIRT,
    "p": Tile.PIPE,
    "t": Tile.PIPE_TOP,
    "s": Tile.BLOCK,
    "q": Tile.COIN_BLOCK,
}
_tiles_ = """
# intro area
bcaaaaaaaa
bcasaaaaaa
bcaasaaaaa
bcaaasaaaa
bcaaaasaaa
bcaaasaaaa
bcaasaaaaa
bcasaaaaaa
bcaaaaaaaa
"""


def parse_map_tiles_string(map_tiles_string):
    # we need to 2d array of tiles
    # probably have build it column by column then transpose it

    columns = []
    for line in map_tiles_string.split("\n"):
        col = []
        if line == "":
            continue
        if line[0] == "#":
            continue
        for c in line:
            col.append(_tile_key_[c])
