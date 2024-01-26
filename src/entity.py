from enum import Enum, auto
import glm


class EntityType(Enum):
    PLAYER = auto()
    GOOMBA = auto()


class DisplayState(Enum):
    IDLE = auto()
    WALKING = auto()
    RUNNING = auto()
    JUMPING = auto()
    FALLING = auto()
    STUNNED = auto()
    DEAD = auto()


class Entity:
    def __init__(self) -> None:
        self.type = None
        self.pos = glm.vec2(6, 6)
        self.size = glm.vec2(8, 8)
        self.vel = glm.vec2(0, 0)
        self.acc = glm.vec2(0, 0)
        self.input_controlled = False
        self.display_state = DisplayState.IDLE
        self.sprite_animator = None
