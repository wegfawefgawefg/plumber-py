import glm
from entity_templates import player_template
from stage import Stage
from stages.level_building import air, floor
from stages.stages import Stages
from tiles import TILE_SIZE, Tile


def a_a():
    stage = Stage()
    floor_level = 2

    ####    TILES   ####
    t = air(16)
    t = floor(t, floor_level, Tile.BRICK)
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

    # add
    flower = Decoration(
        glm.vec2(0, floor_decoration_height),
        SpriteAnimator(
            SpriteFamily.DECORATIONS,
            glm.uvec2(0, 0),
            glm.uvec2(1, 1),
            0.1,
            DisplayState.FOREGROUND,
        ),
    )

    return stage
