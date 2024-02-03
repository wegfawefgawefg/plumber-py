import random
import glm
from ai import (
    ChangeDirectionWhenImpeded,
    PatrolForDuration,
    WalkLeftOrRight,
    WalkRandomlySometimes,
)
from components import CoyoteTimer
from entity import DisplayState, Entity, EntityType, Facing
from sprites.sprite_animator import SpriteAnimator
from sprites.sprite_definitions import (
    GOOMBA_WALKING,
    GOOMBINI_WALKING,
    GOOMBOR_WALKING,
    PLAYER_STANDING,
    SpriteFamily,
)
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

    player.has_entity_collisions = True
    return player


def goomba_template(tile_pos):
    goomba = Entity()
    goomba.type = EntityType.GOOMBA
    goomba.pos = glm.vec2(tile_pos.x * TILE_SIZE, tile_pos.y * TILE_SIZE)
    goomba.size = glm.vec2(13, 14)
    goomba.vel = glm.vec2(0, 0)
    goomba.acc = glm.vec2(0, 0)
    # goomba.input_controlled = True
    goomba.display_state = DisplayState.NEUTRAL
    goomba.sprite_animator = SpriteAnimator(
        SpriteFamily.GOOMBA,
        GOOMBA_WALKING,
    )
    goomba.input_controlled = False
    goomba.has_entity_collisions = True
    # goomba.ai = WalkRandomlySometimes()
    # goomba.ai = PatrolForDuration()
    goomba.ai = ChangeDirectionWhenImpeded()

    goomba.hp = 1
    goomba.facing = random.choice((Facing.LEFT, Facing.RIGHT))

    return goomba


def goombini_template(tile_pos):
    goombini = Entity()
    goombini.type = EntityType.GOOMBINI
    goombini.pos = glm.vec2(tile_pos.x * TILE_SIZE, tile_pos.y * TILE_SIZE)
    goombini.size = glm.vec2(6, 7)
    goombini.vel = glm.vec2(0, 0)
    goombini.acc = glm.vec2(0, 0)
    # goombini.input_controlled = (True,)
    goombini.display_state = DisplayState.NEUTRAL
    goombini.sprite_animator = SpriteAnimator(
        SpriteFamily.GOOMBINI,
        GOOMBINI_WALKING,
    )
    goombini.input_controlled = False
    goombini.has_entity_collisions = True
    # goombini.ai = WalkRandomlySometimes()
    goombini.ai = PatrolForDuration()
    goombini.hp = 1
    goombini.facing = random.choice((Facing.LEFT, Facing.RIGHT))

    return goombini


def goombor_template(tile_pos):
    goombor = Entity()
    goombor.type = EntityType.GOOMBOR
    goombor.pos = glm.vec2(tile_pos.x * TILE_SIZE, tile_pos.y * TILE_SIZE)
    goombor.size = glm.vec2(26, 28)
    goombor.vel = glm.vec2(0, 0)
    goombor.acc = glm.vec2(0, 0)
    goombor.input_controlled = (True,)
    goombor.display_state = DisplayState.NEUTRAL
    goombor.sprite_animator = SpriteAnimator(
        SpriteFamily.GOOMBOR,
        GOOMBOR_WALKING,
    )
    goombor.input_controlled = False
    goombor.has_entity_collisions = True
    goombor.ai = ChangeDirectionWhenImpeded()
    goombor.hp = 1
    goombor.facing = random.choice((Facing.LEFT, Facing.RIGHT))

    return goombor
