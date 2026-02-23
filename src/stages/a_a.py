import inspect
import random
import glm
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

    # spawn some goombas
    # for i in range(0, 100):
    #     # random tile position in map
    #     # x = random.randint(0, (stage.dims.x // 10) - 1)
    #     x = random.randint(0, (stage.dims.x) - 1)
    #     y = 0

    #     goomba = goomba_template(glm.ivec2(x, y))
    #     stage.entities.append(goomba)

    # spawn a goomba on every tile above the floor
    for _ in range(1):
        for y in range(1, int(stage.dims.y) - 1):
            for x in range(1, int(stage.dims.x) - 1):
                tile = stage.get_tile(x, y)
                if tile == Tile.AIR:
                    pos = glm.vec2(x, y)

                    if random.random() < 0.05:
                        which = random.random()
                        if which < 0.2:
                            e = goombini_template(pos)
                        elif which < 0.8:
                            e = goomba_template(pos)
                        else:
                            e = goombor_template(pos)
                        stage.entities.append(e)

    # just a test goomba
    x = 10
    y = 2
    pos = glm.vec2(x, y)
    # e = goombor_template(pos)
    # stage.entities.append(e)
    # e = goomba_template(pos)
    # stage.entities.append(e)
    # e = goombini_template(pos)
    # stage.entities.append(e)

    # player = player_template()
    # player.pos.y -= 10 * TILE_SIZE
    # stage.entities.append(player)

    ####    EXITS   ####
    # stage.add_exit(glm.ivec2(15, 7), Stages.A_A, level_win=True)
    for exit in A_A_EXITS:
        # for exit in TEST_TILES_EXITS:
        pos, next_level, level_win = exit
        stage.add_exit(pos, next_level, level_win)

    ####    DECORATIONS     ####
    # lets add some flowers and mini hills at the floor level
    decorate_floor(stage)

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
bceaaaaaaa
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
