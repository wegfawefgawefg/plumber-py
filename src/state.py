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
        item.lifetime -= 1
    return [item for item in collection if item.lifetime > 0]


class State:
    def __init__(self) -> None:
        self.mode = Mode.PLAYING

        self.entities = []
        self.stage: Stage = None

        self.events = []
        self.special_effects = []

        self.debug_messages: list[str] = []
        self.alerts: list[Message] = []

        self.center_cam_on_player = True

    def load_stage(self, stage):
        self.stage = stage
        self.entities = stage.entities

    def step_alerts(self):
        self.alerts = step_and_cleanse(self.alerts)
