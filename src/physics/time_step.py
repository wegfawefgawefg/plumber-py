from physics.config import MAX_FRAME_TIME_SECONDS, MAX_SIM_STEPS_PER_FRAME, SIMULATION_HZ


class FixedStepAccumulator:
    def __init__(self, simulation_hz=SIMULATION_HZ):
        self.simulation_hz = simulation_hz
        self.fixed_dt = 1.0 / simulation_hz
        self.accumulator = 0.0

    def add_elapsed(self, elapsed_seconds):
        elapsed_seconds = max(0.0, min(elapsed_seconds, MAX_FRAME_TIME_SECONDS))
        self.accumulator = min(
            self.accumulator + elapsed_seconds,
            self.fixed_dt * MAX_SIM_STEPS_PER_FRAME,
        )

    def consume_steps(self):
        steps = 0
        while (
            self.accumulator >= self.fixed_dt
            and steps < MAX_SIM_STEPS_PER_FRAME
        ):
            self.accumulator -= self.fixed_dt
            steps += 1
        return steps

    def alpha(self):
        if self.fixed_dt <= 0.0:
            return 1.0
        return max(0.0, min(self.accumulator / self.fixed_dt, 1.0))
