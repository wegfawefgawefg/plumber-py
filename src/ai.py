from enum import Enum, auto
import random


class AI:
    pass


class StayStillOrWalk(Enum):
    STAY_STILL = auto()
    WALK = auto()


class WalkRandomlySometimes(AI):
    DURATION_RANGE = 200
    WALK_FORCE = 0.01

    def __init__(self) -> None:
        super().__init__()
        self.mode: StayStillOrWalk = StayStillOrWalk.STAY_STILL
        self.timer = 0
        self.direction = 0

    def step(self, entity):
        if entity.hp <= 0:
            return

        if self.timer == 0:
            new_mode = random.choice((StayStillOrWalk.WALK, StayStillOrWalk.STAY_STILL))
            self.mode = new_mode
            match self.mode:
                case StayStillOrWalk.STAY_STILL:
                    self.timer = random.randint(0, WalkRandomlySometimes.DURATION_RANGE)
                case StayStillOrWalk.WALK:
                    self.timer = random.randint(0, WalkRandomlySometimes.DURATION_RANGE)
                    self.direction = random.choice((-1, 1))
        else:
            if self.timer > 0:
                self.timer -= 1
        match self.mode:
            case StayStillOrWalk.STAY_STILL:
                pass
            case StayStillOrWalk.WALK:
                entity.acc.x += WalkRandomlySometimes.WALK_FORCE * self.direction
