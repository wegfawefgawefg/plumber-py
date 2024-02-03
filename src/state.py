from enum import Enum, auto
from entity import get_entity_bounds

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
        self.active_entities = []
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

    def set_active_entities(self, camera):
        self.active_entities.clear()

        ctl = camera.pos
        cbr = camera.pos + camera.size

        for entity in self.entities:
            if entity.always_active:
                self.active_entities.append(entity)
                continue
            entity_tl, entity_br = get_entity_bounds(entity.pos, entity.size)
            if entity_br.x < (ctl.x - 1):
                continue
            # if entity_br.y < ctl.y:
            #     continue
            if entity_tl.x > cbr.x:
                continue
            if entity_tl.y > cbr.y:
                continue
            self.active_entities.append(entity)
