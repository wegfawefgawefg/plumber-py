from enum import Enum, auto
import random

from audio import PlaySound, Sounds


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

    def step(self, entity, state, graphics, audio):
        if entity.hp <= 0:
            # entity.size.y = 11
            entity.size.y = 6
            entity.vel.x = 0
            return

        if self.timer == 0:
            # 1 in 5 chance to become dead
            if random.randint(0, 5) == 0:
                audio.events.append(
                    PlaySound(
                        random.choice(
                            (
                                Sounds.GOOMBA_CRY,
                                Sounds.GOOMBA_CRY_HIGH,
                                Sounds.GOOMBA_CRY_LOW,
                            )
                        )
                    )
                )
                # entity.hp = 0
                # return

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


class WalkLeftOrRight(Enum):
    WALK_LEFT = auto()
    WALK_RIGHT = auto()


class PatrolForDuration(AI):
    DURATION = 60
    WALK_FORCE = 0.01

    def __init__(self) -> None:
        super().__init__()
        self.mode: WalkLeftOrRight = random.choice(
            (WalkLeftOrRight.WALK_LEFT, WalkLeftOrRight.WALK_RIGHT)
        )
        self.timer = 0

    def step(self, entity, state, graphics, audio):
        if self.timer == 0:
            audio.events.append(
                PlaySound(
                    random.choice(
                        (
                            Sounds.GOOMBA_CRY,
                            Sounds.GOOMBA_CRY_HIGH,
                            Sounds.GOOMBA_CRY_LOW,
                        )
                    )
                )
            )

            match self.mode:
                case WalkLeftOrRight.WALK_LEFT:
                    self.mode = WalkLeftOrRight.WALK_RIGHT
                    self.timer = PatrolForDuration.DURATION
                    entity.vel.x = 0
                case WalkLeftOrRight.WALK_RIGHT:
                    self.mode = WalkLeftOrRight.WALK_LEFT
                    self.timer = PatrolForDuration.DURATION
                    entity.vel.x = 0

        if self.timer > 0:
            self.timer -= 1
        match self.mode:
            case WalkLeftOrRight.WALK_LEFT:
                entity.acc.x -= PatrolForDuration.WALK_FORCE
            case WalkLeftOrRight.WALK_RIGHT:
                entity.acc.x += PatrolForDuration.WALK_FORCE


class ChangeDirectionWhenImpeded(AI):
    WALK_FORCE = 0.01

    def __init__(self) -> None:
        super().__init__()
        self.mode: WalkLeftOrRight = random.choice(
            (WalkLeftOrRight.WALK_LEFT, WalkLeftOrRight.WALK_RIGHT)
        )
        self.old_positions = []

    def step(self, entity, state, graphics, audio):
        if len(self.old_positions) > 2:
            self.old_positions.pop(0)
        self.old_positions.append(int(entity.pos.x))

        # state.debug_messages.append(f"old positions: {self.old_positions}")
        # state.debug_messages.append(f"vel: {entity.vel.x}")

        vel_clause = abs(entity.vel.x) < 0.001
        old_positions_clause = len(self.old_positions) == 3
        # state.debug_messages.append(f"vel clause: {vel_clause}")
        # state.debug_messages.append(f"old positions clause: {old_positions_clause}")
        if vel_clause and old_positions_clause:
            all_equal = all(x == self.old_positions[0] for x in self.old_positions)
            if all_equal:
                match self.mode:
                    case WalkLeftOrRight.WALK_LEFT:
                        self.mode = WalkLeftOrRight.WALK_RIGHT
                    case WalkLeftOrRight.WALK_RIGHT:
                        self.mode = WalkLeftOrRight.WALK_LEFT
                self.old_positions.clear()

        match self.mode:
            case WalkLeftOrRight.WALK_LEFT:
                entity.acc.x -= ChangeDirectionWhenImpeded.WALK_FORCE
            case WalkLeftOrRight.WALK_RIGHT:
                entity.acc.x += ChangeDirectionWhenImpeded.WALK_FORCE
