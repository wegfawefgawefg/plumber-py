import random
import glm
from ai import WalkRandomlySometimes
from components import CoyoteTimer
from entity import DisplayState, Entity, EntityType, Facing
from sprites.sprite_animator import SpriteAnimator
from sprites.sprite_definitions import GOOMBA_WALKING, PLAYER_STANDING, SpriteFamily
from tiles import TILE_SIZE


def player_template():
    player = Entity()
    player.type = EntityType.PLAYER
    player.pos = glm.vec2(4 * TILE_SIZE, 2 * TILE_SIZE)
    player.size = glm.vec2(8, 12)

    player.vel = glm.vec2(0, 0)
    player.acc = glm.vec2(0, 0)
    player.input_controlled = (True,)
    player.display_state = DisplayState.NEUTRAL
    player.sprite_animator = SpriteAnimator(
        SpriteFamily.PLAYER,
        PLAYER_STANDING,
    )

    player.coyote_timer = CoyoteTimer(6)
    player.always_active = True
    return player


def goomba_template(tile_pos):
    goomba = Entity()
    goomba.type = EntityType.GOOMBA
    goomba.pos = glm.vec2(tile_pos.x * TILE_SIZE, tile_pos.y * TILE_SIZE)
    goomba.size = glm.vec2(14, 15)
    goomba.vel = glm.vec2(0, 0)
    goomba.acc = glm.vec2(0, 0)
    goomba.input_controlled = (True,)
    goomba.display_state = DisplayState.NEUTRAL
    goomba.sprite_animator = SpriteAnimator(
        SpriteFamily.GOOMBA,
        GOOMBA_WALKING,
    )
    goomba.input_controlled = False
    goomba.ai = WalkRandomlySometimes()
    goomba.hp = 0
    goomba.facing = random.choice((Facing.LEFT, Facing.RIGHT))

    return goomba
