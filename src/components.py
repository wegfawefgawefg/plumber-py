class CoyoteTimer:
    def __init__(self, duration):
        self.duration = duration
        self.timer = 0

    def step(self):
        if self.timer > 0:
            self.timer -= 1

    def can_jump(self):
        return self.timer > 0

    def reset(self):
        self.timer = self.duration
