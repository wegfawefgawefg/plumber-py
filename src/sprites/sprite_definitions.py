from enum import Enum, auto

import glm
from entity import DisplayState

from graphics import Textures
from sprites.serially_stored_animated_sprite import SeriallyStoredAnimatedSprite
from sprites.sprite import Sprite
from sprites.static_sprite import StaticSprite

###################################################################################
##########################    ENTITY STUFF                 ########################
###################################################################################
# ////////////////////////    ENTITY SPRITE DEFINITIONS    ////////////////////////
DEFAULT = StaticSprite(
    Textures.ENTITIES,
    glm.vec2(0, 48),
    glm.vec2(16, 16),
)

PLAYER_STANDING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(0, 0),
    glm.vec2(16, 16),
    glm.vec2(-4, -4),
    2,
    True,
)

PLAYER_WALKING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(32, 0),
    glm.vec2(16, 16),
    glm.vec2(-4, -4),
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

GOOMBA_WALKING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 16),
    glm.vec2(16, 16),
    glm.vec2(-2, -2),
    4,
    True,
)

GOOMBA_DEAD = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 32),
    glm.vec2(16, 16),
    glm.vec2(-2, -5),
    11,
    False,
)

GOOMBINI_WALKING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 48),
    glm.vec2(16, 16),
    glm.vec2(-5, -9),
    4,
    True,
)

GOOMBINI_DEAD = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 64),
    glm.vec2(16, 16),
    glm.vec2(-5, -11),
    11,
    False,
)

GOOMBOR_WALKING = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 80),
    glm.vec2(32, 32),
    glm.vec2(-4, -4),
    4,
    True,
)

GOOMBOR_DEAD = SeriallyStoredAnimatedSprite(
    Textures.ENTITIES,
    glm.vec2(64, 32),
    glm.vec2(32, 32),
    glm.vec2(-4, -4),
    11,
    False,
)


# ////////////////////////    ENTITY SPRITE FAMILIES    ////////////////////////
class SpriteFamily(Enum):
    PLAYER = auto()
    BAT = auto()
    GOOMBA = auto()
    GOOMBINI = auto()
    GOOMBOR = auto()


def get_sprite_for_display_state_given_family(
    family: SpriteFamily, display_state: DisplayState
) -> Sprite:
    match family:
        case SpriteFamily.PLAYER:
            match display_state:
                case DisplayState.NEUTRAL:
                    return PLAYER_STANDING
                case DisplayState.WALKING:
                    return PLAYER_WALKING
                case DisplayState.FALLING:
                    return PLAYER_FALLING
                case DisplayState.CLIMBING:
                    return PLAYER_CLIMBING
                case DisplayState.STUNNED:
                    return PLAYER_STUNNED
                case DisplayState.DEAD:
                    return PLAYER_DEAD
        case SpriteFamily.GOOMBA:
            match display_state:
                case DisplayState.WALKING:
                    return GOOMBA_WALKING
                case DisplayState.DEAD:
                    return GOOMBA_DEAD
                case _:
                    return GOOMBA_WALKING
        case SpriteFamily.GOOMBINI:
            match display_state:
                case DisplayState.WALKING:
                    return GOOMBINI_WALKING
                case DisplayState.DEAD:
                    return GOOMBINI_DEAD
                case _:
                    return GOOMBINI_WALKING
        case SpriteFamily.GOOMBOR:
            match display_state:
                case DisplayState.WALKING:
                    return GOOMBOR_WALKING
                case DisplayState.DEAD:
                    return GOOMBOR_DEAD
                case _:
                    return GOOMBOR_WALKING

        case _:
            raise ValueError("Invalid sprite family")


###################################################################################
##########################    DECORATIONS STUFF            ########################
###################################################################################
# ////////////////////////   DECORATION SPRITE DEFINITIONS ////////////////////////
FLOWER = SeriallyStoredAnimatedSprite(
    Textures.DECORATIONS,
    glm.vec2(0, 0),
    glm.vec2(16, 16),
    glm.vec2(0, 0),
    2,
    True,
)

MINI_HILL = StaticSprite(
    Textures.DECORATIONS,
    glm.vec2(0, 16),
    glm.vec2(16, 16),
)

BIG_PIPE = StaticSprite(
    Textures.DECORATIONS,
    glm.vec2(16, 16),
    glm.vec2(32, 32),
)
