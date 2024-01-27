from enum import Enum, auto

import glm

TILE_SIZE = 16


class Tile(Enum):
    AIR = auto()
    BRICK = auto()
    EXIT = auto()
    SPIKES = auto()


COLLIDEABLE_TILES = set((Tile.BRICK,))


def is_tile_collidable(tile):
    if tile in COLLIDEABLE_TILES:
        return True
    return False


TRANSPARENT_TILES = set((Tile.EXIT, Tile.SPIKES))


def is_tile_transparent(tile):
    if tile in TRANSPARENT_TILES:
        return True
    return False


TILE_TEXTURE_SAMPLE_POSITIONS = {
    Tile.AIR: glm.uvec2(0, 0),
    Tile.BRICK: glm.uvec2(0, 1),
    Tile.EXIT: glm.uvec2(0, 9),
    Tile.SPIKES: glm.uvec2(0, 6),
}


def get_tile_texture_sample_position(tile) -> glm.uvec2:
    return TILE_TEXTURE_SAMPLE_POSITIONS[tile]


def collidable_tile_in_list(tiles):
    for tile in tiles:
        collided = is_tile_collidable(tile)
        if collided:
            return True
    return False
