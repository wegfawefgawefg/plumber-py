import inspect
import random
import glm
from entity import Facing
from entity_templates import (
    goomba_template,
    goombini_template,
    goombor_template,
    player_template,
)
from sprites.sprite_animator import BasicSpriteAnimator
from sprites.sprite_definitions import FLOWER, MINI_HILL
from stage import Decoration, Exit, Stage
from stages.level_building import (
    ForegroundOrBackground,
    air,
    decorate_floor,
    floor,
    foreground_or_background,
    parse_map_tiles_string,
    where_are_the_exits,
)
from stages.stages import Stages
from tiles import TILE_SIZE, Tile, is_tile_collidable


TEST_ARENA_WIDTH_TILES = 32
TEST_ARENA_HEIGHT_TILES = 16


def _enclosed_arena_tiles(width_tiles, height_tiles):
    tiles = [[Tile.AIR for _ in range(width_tiles)] for _ in range(height_tiles)]

    for x in range(width_tiles):
        tiles[0][x] = Tile.DIRT
        tiles[height_tiles - 1][x] = Tile.DIRT

    for y in range(height_tiles):
        tiles[y][0] = Tile.DIRT
        tiles[y][width_tiles - 1] = Tile.DIRT

    return tiles


def _spawn_test_entities(stage):
    # Anchor target: heavy/large body that cannot be pushed or squished.
    goombor = goombor_template(glm.vec2(17, 12))
    goombor.can_be_pushed = False
    goombor.can_be_squished = False
    goombor.facing = Facing.LEFT
    stage.entities.append(goombor)

    # Mid-size pushers: can push and can also be squished.
    for tile_pos in (glm.vec2(9, 12), glm.vec2(11, 12), glm.vec2(13, 12)):
        goombini = goombini_template(tile_pos)
        goombini.can_push_entities = True
        goombini.can_be_pushed = True
        goombini.can_be_squished = True
        stage.entities.append(goombini)

    # Standard goomba: pushable and squishable.
    goomba = goomba_template(glm.vec2(15, 12))
    goomba.can_be_pushed = True
    goomba.can_be_squished = True
    stage.entities.append(goomba)


def a_a():
    stage = Stage()

    ####    TILES   ####
    t = _enclosed_arena_tiles(TEST_ARENA_WIDTH_TILES, TEST_ARENA_HEIGHT_TILES)
    stage.set_tiles(t)

    ####    ENTITIES    ####
    player = player_template()
    player.pos = glm.vec2(2 * TILE_SIZE, 2 * TILE_SIZE)
    stage.entities.append(player)
    _spawn_test_entities(stage)

    ####    EXITS   ####
    # stage.add_exit(glm.ivec2(15, 7), Stages.A_A, level_win=True)
    # for exit in A_A_EXITS:
    # for exit in TEST_TILES_EXITS:
    #     pos, next_level, level_win = exit
    #     stage.add_exit(pos, next_level, level_win)

    ####    DECORATIONS     ####
    # lets add some flowers and mini hills at the floor level
    # decorate_floor(stage)

    return stage


# is a comment line

TEST_TILES_EXITS = [
    (glm.ivec2(6, 7), Stages.A_A, True),
]
TEST_TILES_LINE_NUMBER = 78
TEST_TILES = """
bcaaaaaaaa
bcaaaaaaaa
bbbbbcaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bbbbbcaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
"""

A_A_EXITS = [
    (glm.ivec2(189, 7), Stages.A_A, True),
]
A_A_TILES_LINE_NUMBER = 107
A_A_TILES = """
# intro area
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# coin block and coin pyramid
bcaqaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcasaaaaaa
bcaqaaaaaa
bcasaqaaaa
bcaqaaaaaa
bcasaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# pipe hurdles
bctaaaaaaa
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa
bcptaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa
bcpptaaaaa
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa
bcpptaaaaa

# first floor gap
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
aaaaaaaaaa
aaaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# 2 layer gap walk
bcaaaaaaaa
bcasaaaaaa
bcaqaaaaaa
bcasaaaaaa
bcaaasaaaa
bcaaasaaaa
bcaaasaaaa
bcaaasaaaa
bcaaasaaaa
aaaaasaaaa
aaaaasaaaa
aaaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaasaaaa
bcaaasaaaa
bcaaasaaaa
bcasaqaaaa

# some blocks and another  coin block pyramid
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaasaaaaa
bcaaqaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaqaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaqaqaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaqaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# 2 layer gap walk round 2
bcaasaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaasaaaa
bcaaasaaaa
bcaaasaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaasaaaa
bcasaqaaaa
bcasaqaaaa
bcaaasaaaa
bcaaaaaaaa
bcaaaaaaaa

# block pyramid
bcsaaaaaaa
bcssaaaaaa
bcsssaaaaa
bcsaaaaaaa
bcsaaaaaaa
bcsssaaaaa
bcssaaaaaa
bcsaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# block pyramid with void
bcsaaaaaaa
bcssaaaaaa
bcsssaaaaa
bcssssaaaa
aaaaaaaaaa
aaaaaaaaaa
bcssssaaaa
bcsssaaaaa
bcssaaaaaa
bcsaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# pipe homage
bcptaaaaaa
bcptaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaasaaaaa
bcaasaaaaa
bcaaqaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa

# pipe then block ramp to end
bcptaaaaaa
bcptaaaaaa
bcsaaaaaaa
bcssaaaaaa
bcsssaaaaa
bcssssaaaa
bcsssssaaa
bcssssssaa

# end
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bceaaaaaaa

bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bbbbbbbbbb  
"""

if __name__ == "__main__":
    tiles = parse_map_tiles_string(A_A_TILES, A_A_TILES_LINE_NUMBER)
    where_are_the_exits(tiles)
