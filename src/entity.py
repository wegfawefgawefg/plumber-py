from enum import Enum, auto
import glm

from tiles import TILE_SIZE


class EntityType(Enum):
    PLAYER = auto()
    GOOMBA = auto()
    GOOMBINI = auto()
    GOOMBOR = auto()


class DisplayState(Enum):
    NEUTRAL = auto()
    WALKING = auto()
    JUMPING = auto()
    FALLING = auto()
    CLIMBING = auto()
    STUNNED = auto()
    DEAD = auto()


class Facing(Enum):
    LEFT = auto()
    RIGHT = auto()


class Entity:
    def __init__(self) -> None:
        self.type = None
        self.pos = glm.vec2(6, 6)
        self.size = glm.vec2(8, 8)
        self.vel = glm.vec2(0, 0)
        self.acc = glm.vec2(0, 0)
        self.input_controlled = False
        self.display_state = DisplayState.NEUTRAL
        self.sprite_animator = None
        self.no_gravity = False
        self.facing = Facing.RIGHT
        self.has_tile_collisions = True
        self.has_entity_collisions = True
        self.grounded = False
        self.always_active = False
        self.is_sticky_platform = (
            False  # is true if the entity moves entities on top of it
        )
        self.stun_timer = 0
        self.hp = 1
        self.invincible = False

        # optional components
        self.coyote_timer = None
        self.ai = None

    def __repr__(self) -> str:
        return f"Entity({self.type})"


###################### UTILS ######################


def get_entity_bounds(pos, size):
    tl = pos
    br = pos + size - glm.vec2(1, 1)
    return tl, br


def get_entity_feet(pos, size):
    entity_tl, entity_br = get_entity_bounds(pos, size)
    feet_tl = glm.vec2(entity_tl.x + 1, entity_br.y)
    feet_br = entity_br + glm.vec2(0, 1)
    return feet_tl, feet_br


def get_tiles_at_feet(pos, size, state):
    feet_tl, feet_br = get_entity_feet(pos, size)
    # get tiles in player bounds
    feet_tl_tile_pos = feet_tl / TILE_SIZE
    feet_br_tile_pos = feet_br / TILE_SIZE
    tiles_at_feet = state.stage.get_tiles_in_rect(feet_tl_tile_pos, feet_br_tile_pos)
    return tiles_at_feet


def intersects(tl, br, otl, obr):
    return not (br.x < otl.x or tl.x > obr.x or br.y < otl.y or tl.y > obr.y)
