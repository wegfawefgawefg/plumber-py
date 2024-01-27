from enum import Enum, auto

from stages import a_a, a_b


class Stages(Enum):
    A_A = auto()
    A_B = auto()


STAGE_CONSTRUCTORS = {
    Stages.A_A: a_a,
    Stages.A_B: a_b,
}
