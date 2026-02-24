from enum import Enum, auto
import glm
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
        self.frame = 0
        self.render_alpha = 1.0

        self.entities = []
        self.active_entities = []
        self.stage: Stage = None

        self.events = []
        self.physics_events = []
        self._physics_event_keys = set()
        self.special_effects = []

        self.debug_messages: list[str] = []
        self.alerts: list[Message] = []

        self.center_cam_on_player = True

    def load_stage(self, stage):
        self.stage = stage
        self.entities = stage.entities

    def step_alerts(self):
        self.alerts = step_and_cleanse(self.alerts)

    def reset_physics_events(self):
        self.physics_events.clear()
        self._physics_event_keys.clear()

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

    def snapshot_previous_transforms(self, graphics):
        for entity in self.entities:
            entity.prev_pos = glm.vec2(entity.pos)
        graphics.camera.prev_pos = glm.vec2(graphics.camera.pos)
