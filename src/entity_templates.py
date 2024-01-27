import glm
from components import CoyoteTimer
from entity import DisplayState, Entity, EntityType
from sprites.sprite_animator import SpriteAnimator
from sprites.sprite_definitions import PLAYER_STANDING, SpriteFamily
from tiles import TILE_SIZE


def player_template():
    player = Entity()
    player.type = EntityType.PLAYER
    player.pos = glm.vec2(4 * TILE_SIZE, 2 * TILE_SIZE)
    player.size = glm.vec2(8, 12)
    player.vel = glm.vec2(0, 0)
    player.acc = glm.vec2(0, 0)
    player.input_controlled = (True,)
    player.display_state = DisplayState.IDLE
    player.sprite_animator = SpriteAnimator(
        SpriteFamily.PLAYER,
        PLAYER_STANDING,
    )
    player.sprite_animator.frame_duration = 12

    player.coyote_timer = CoyoteTimer(6)
    return player
