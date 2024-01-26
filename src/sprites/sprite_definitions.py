from enum import Enum, auto

import glm
from entity import DisplayState

from graphics import Textures
from sprites.serially_stored_animated_sprite import SeriallyStoredAnimatedSprite
from sprites.sprite import Sprite
from sprites.static_sprite import StaticSprite

# ////////////////////////    SPRITE DEFINITIONS    ////////////////////////
DEFAULT = StaticSprite(
    Textures.ENTITIES,
    glm.vec2(0, 48),
    glm.vec2(16, 16),
)

PLAYER_STANDING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(0, 0),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

PLAYER_WALKING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(32, 16),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

PLAYER_DEAD = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 16),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

PLAYER_STUNNED = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(96, 16),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

PLAYER_CLIMBING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(128, 16),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

PLAYER_FALLING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(160, 16),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)


# ////////////////////////    SPRITE FAMILIES    ////////////////////////
class SpriteFamily(Enum):
    PLAYER = auto()
    BAT = auto()


def get_sprite_for_display_state_given_family(
    family: SpriteFamily, display_state: DisplayState
) -> Sprite:
    match family:
        case SpriteFamily.PLAYER:
            match display_state:
                case DisplayState.Neutral:
                    return PLAYER_STANDING
                case DisplayState.Walk:
                    return PLAYER_WALKING
                case DisplayState.Dead:
                    return PLAYER_DEAD
                case DisplayState.Stunned:
                    return PLAYER_STUNNED
                case DisplayState.Falling:
                    return PLAYER_FALLING
                case DisplayState.Climbing:
                    return PLAYER_CLIMBING
