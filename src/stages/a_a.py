import random
import glm
from entity_templates import player_template
from sprites.sprite_animator import BasicSpriteAnimator
from sprites.sprite_definitions import FLOWER, MINI_HILL
from stage import Decoration, Stage
from stages.level_building import (
    ForegroundOrBackground,
    air,
    floor,
    foreground_or_background,
)
from stages.stages import Stages
from tiles import TILE_SIZE, Tile


def a_a():
    stage = Stage()
    floor_level = 2
    stage_width = 64  # 16

    ####    TILES   ####
    t = air(stage_width)
    t = floor(t, floor_level, Tile.CAPPED_DIRT, Tile.DIRT)
    # t = random_bumps(t, 13, 0.1)
    # t = random_bumps(t, 10, 0.1)
    stage.set_tiles(t)

    ####    ENTITIES    ####
    player = player_template()
    stage.entities.append(player)

    ####    EXITS   ####
    stage.add_exit(glm.ivec2(15, 7), Stages.A_A, level_win=True)

    ####    DECORATIONS     ####
    # lets add some flowers and mini hills at the floor level
    floor_height = 10 - floor_level
    floor_decoration_height_tile = floor_height - 1
    floor_decoration_height = floor_decoration_height_tile * TILE_SIZE

    flower_chance = 0.1
    mini_hill_chance = 0.1
    for c in range(0, stage_width):
        layer = foreground_or_background()

        item = None
        if random.random() < flower_chance:
            item = Decoration(
                glm.vec2(c * TILE_SIZE, floor_decoration_height),
                BasicSpriteAnimator(FLOWER),
            )

        elif random.random() < mini_hill_chance:
            item = Decoration(
                glm.vec2(c * TILE_SIZE, floor_decoration_height),
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

_tiles_ = """
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
bcaaqaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaasaaaaa
bcaaqaaaaa
bcaasaaqaa
bcaaqaaaaa
bcaasaaaaa
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
baaaaaaaaa 
bcaaaaaaaa
bcpptaaaaa
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bcaaaaaaaa 
bbcaaaaaaa 
bbcaaaaaaa 
baaaaaaaaa 
bcaaaaaaaa
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
bcaaqaaqaa
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
bcaaaasaaa
bcaaaasaaa
bcaaaasaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaaaaaa
bcaaaasaaa
bcaasaqaaa
bcaasaqaaa
bcaaaasaaa
bcaaaaaaaa
bcaaaaaaaa

# block pyramid
bcsaaaaaaa
bcssaaaaaa
bcsssaaaaa
bcssssaaaa
bcsaaaaaaa
bcsaaaaaaa
bcssssaaaa
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