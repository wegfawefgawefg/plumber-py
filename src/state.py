from enum import Enum, auto


class Mode(Enum):
    PAUSE = auto()
    PLAYING = auto()


class State:
    def __init__(self) -> None:
        self.mode = Mode.PLAYING

        self.entities = []
        self.stage = None

    def load_stage(self, stage):
        self.stage = stage
        self.entities = stage.entities
