import inspect
import random
import glm
from entity_templates import player_template
from sprites.sprite_animator import BasicSpriteAnimator
from sprites.sprite_definitions import FLOWER, MINI_HILL
from stage import Decoration, Exit, Stage
from stages.level_building import (
    ForegroundOrBackground,
    air,
    floor,
    foreground_or_background,
    parse_map_tiles_string,
    where_are_the_exits,
)
from stages.stages import Stages
from tiles import TILE_SIZE, Tile


def a_a():
    stage = Stage()

    ####    TILES   ####
    t = parse_map_tiles_string(A_A_TILES, A_A_TILES_LINE_NUMBER)
    # t = parse_map_tiles_string(TEST_TILES, TEST_TILES_LINE_NUMBER)
    # t = air(stage_width)
    # t = floor(t, floor_level, Tile.CAPPED_DIRT, Tile.DIRT)
    # t = random_bumps(t, 13, 0.1)
    # t = random_bumps(t, 10, 0.1)
    stage.set_tiles(t)

    ####    ENTITIES    ####
    player = player_template()
    stage.entities.append(player)

    ####    EXITS   ####
    # stage.add_exit(glm.ivec2(15, 7), Stages.A_A, level_win=True)
    for exit in A_A_EXITS:
        pos, next_level, level_win = exit
        stage.add_exit(pos, next_level, level_win)

    ####    DECORATIONS     ####
    # lets add some flowers and mini hills at the floor level

    flower_chance = 0.3
    mini_hill_chance = 0.1
    # check every tile in the stage, and if its a Tile. CAPPED_DIRT, add a flower or mini hill
    for r, row in enumerate(stage.tiles):
        for c, col in enumerate(row):
            if col != Tile.CAPPED_DIRT:
                continue

            pos = glm.vec2(c, r - 1)

            layer = foreground_or_background()

            item = None
            if random.random() < flower_chance:
                item = Decoration(
                    glm.vec2(pos.x * TILE_SIZE, pos.y * TILE_SIZE),
                    BasicSpriteAnimator(FLOWER),
                )

            elif random.random() < mini_hill_chance:
                item = Decoration(
                    glm.vec2(pos.x * TILE_SIZE, pos.y * TILE_SIZE),
                    BasicSpriteAnimator(MINI_HILL),
                )

            if item is not None:
                item.sprite_animator.frame_duration *= 4
                match layer:
                    case ForegroundOrBackground.FOREGROUND:
                        stage.foreground_decorations.append(item)
                    case ForegroundOrBackground.BACKGROUND:
                        stage.background_decorations.append(item)

    return stage


# is a comment line

TEST_TILES_EXITS = [
    (glm.ivec2(6, 7), Stages.A_A, True),
]
TEST_TILES_LINE_NUMBER = 78
TEST_TILES = """
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
