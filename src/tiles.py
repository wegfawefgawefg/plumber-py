from enum import Enum, auto

import glm

TILE_SIZE = 16


class Tiles(Enum):
    AIR = auto()
    BRICK = auto()
    WIN = auto()
    SPIKES = auto()


def is_tile_collidable(tile):
    match tile:
        case Tiles.AIR:
            return False
        case Tiles.BRICK:
            return True
        case Tiles.WIN:
            return False
        case Tiles.SPIKES:
            return False


def get_tile_texture_sample_position(tile) -> glm.uvec2:
    match tile:
        case Tiles.AIR:
            return glm.uvec2(0, 0)
        case Tiles.BRICK:
            return glm.uvec2(0, 1)
        case Tiles.WIN:
            return glm.uvec2(0, 9)
        case Tiles.SPIKES:
            return glm.uvec2(0, 6)


def collidable_tile_in_list(tiles):
    for tile in tiles:
        collided = is_tile_collidable(tile)
        if collided:
            return True
    return False
