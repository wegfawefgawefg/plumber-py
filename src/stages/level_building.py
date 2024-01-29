from enum import Enum, auto
import inspect
from pprint import pprint
import random

import glm
from sprites.sprite_animator import BasicSpriteAnimator
from sprites.sprite_definitions import FLOWER, MINI_HILL
from stage import Decoration
from tiles import TILE_SIZE, Tile, is_tile_collidable


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


def decorate_floor(stage):
    flower_chance = 0.8
    mini_hill_chance = 0.1
    # check every tile in the stage, and if its a Tile. CAPPED_DIRT, add a flower or mini hill
    for r, row in enumerate(stage.tiles):
        for c, tile in enumerate(row):
            if tile != Tile.CAPPED_DIRT:
                continue

            pos = glm.vec2(c, r - 1)
            tile_at_pos = stage.tiles[int(pos.y)][int(pos.x)]
            if tile_at_pos == Tile.EXIT:
                continue

            layer = foreground_or_background()
            if layer == ForegroundOrBackground.BACKGROUND:
                if is_tile_collidable(tile_at_pos):
                    continue

            item = None
            if random.random() < flower_chance:
                item = Decoration(
                    glm.vec2(pos.x * TILE_SIZE, pos.y * TILE_SIZE),
                    BasicSpriteAnimator(FLOWER),
                    flip=random.random() < 0.5,
                )

            elif random.random() < mini_hill_chance:
                item = Decoration(
                    glm.vec2(pos.x * TILE_SIZE, pos.y * TILE_SIZE),
                    BasicSpriteAnimator(MINI_HILL),
                    flip=random.random() < 0.5,
                )

            if item is not None:
                item.sprite_animator.frame_duration *= 4
                match layer:
                    case ForegroundOrBackground.FOREGROUND:
                        stage.foreground_decorations.append(item)
                    case ForegroundOrBackground.BACKGROUND:
                        stage.background_decorations.append(item)


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

CHAR_TO_TILE_KEY = {
    "a": Tile.AIR,
    "b": Tile.DIRT,
    "c": Tile.CAPPED_DIRT,
    "p": Tile.PIPE,
    "t": Tile.PIPE_TOP,
    "s": Tile.BLOCK,
    "q": Tile.COIN_BLOCK,
    "e": Tile.EXIT,
}


def parse_map_tiles_string(map_tiles_string, definition_line_number):
    # we need to 2d array of tiles
    # probably have build it column by column then transpose it

    valid_chars = set(CHAR_TO_TILE_KEY.keys())

    rows = []
    for li, line in enumerate(map_tiles_string.split("\n")):
        row = []
        if line == "":
            continue
        if line[0] == "#":
            continue
        line = line.strip()
        for c in line:
            if c not in valid_chars:
                raise Exception(
                    f"unknown tile key {c} on {definition_line_number + li}"
                )
            else:
                tile = CHAR_TO_TILE_KEY[c]
                row.append(tile)
        rows.append(row)

    # make sure that it has rows
    if len(rows) == 0:
        raise Exception("no rows in map_tiles_string")
    # make sure it has columns
    if len(rows[0]) == 0:
        raise Exception("no columns in map_tiles_string")

    # transpose, but flip y
    tiles = []
    for c in range(len(rows[0])):
        col = []
        for r in range(len(rows)):
            col.append(rows[r][10 - c - 1])
        tiles.append(col)

    return tiles


def where_are_the_exits(tiles):
    exits = []
    for y, row in enumerate(tiles):
        for x, col in enumerate(row):
            if col == Tile.EXIT:
                exits.append(glm.ivec2(x, y))
    print(exits)


if __name__ == "__main__":
    tiles = parse_map_tiles_string(_tiles_)
    pprint(tiles)
