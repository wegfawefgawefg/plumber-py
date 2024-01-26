from enum import Enum, auto

from stage import Stage


class Mode(Enum):
    PAUSE = auto()
    PLAYING = auto()


class Message:
    def __init__(self, text, lifetime) -> None:
        self.text = text
        self.lifetime = lifetime


def step_and_cleanse(collection):
    for item in collection:
        item.duration -= 1
    return [item for item in collection if item.duration > 0]


class State:
    def __init__(self) -> None:
        self.mode = Mode.PLAYING

        self.entities = []
        self.stage: Stage = None

        self.events = []

        self.debug_messages: list[str] = []
        self.alerts: list[Message] = []

    def load_stage(self, stage):
        self.stage = stage
        self.entities = stage.entities

    def step_alerts(self):
        self.alerts = step_and_cleanse(self.alerts)

    def meta_step(self):
        self.step_alerts()
        self.debug_messages = []
