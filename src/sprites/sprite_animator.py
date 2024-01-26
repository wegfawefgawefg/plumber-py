import random

import glm
from entity import DisplayState
from sprites.sprite import Sprite
from sprites.sprite_definitions import (
    SpriteFamily,
    get_sprite_for_display_state_given_family,
)


DEFAULT_FRAME_DURATION = 4  # animation changes every 4 frames


class SpriteAnimator:
    def __init__(self, sprite_family: SpriteFamily, sprite: Sprite):
        self.sprite_family = sprite_family
        self.sprite = sprite
        self.current_frame = 0
        self.countdown_timer = DEFAULT_FRAME_DURATION
        self.frame_duration = DEFAULT_FRAME_DURATION

    def get_current_frame(self) -> int:
        return self.current_frame

    def get_frame_offset(self) -> glm.vec2:
        return self.sprite.get_frame_offset(self.current_frame)

    def update_sprite_based_on_display_state(self, display_state: DisplayState):
        sprite = get_sprite_for_display_state_given_family(
            self.sprite_family, display_state
        )
        self.set_sprite(sprite)

    def set_sprite(self, sprite: Sprite):
        self.sprite = sprite
        self.current_frame %= sprite.get_num_frames()
        self.countdown_timer = self.frame_duration

    def reset_speed(self):
        self.frame_duration = DEFAULT_FRAME_DURATION

    def restart(self):
        self.current_frame = 0
        self.countdown_timer = self.frame_duration

    def reset_timer(self):
        self.countdown_timer = self.frame_duration

    def randomize_timer(self):
        # add up to 1 less than frame_duration to the timer,
        self.countdown_timer += random.randint(0, self.frame_duration - 1)

    def set_frame_duration(self, frame_duration: int):
        self.frame_duration = max(frame_duration, 1)

    def step(self):
        if not self.sprite.is_animated():
            return

        self.countdown_timer -= 1
        if self.countdown_timer == 0:
            self.countdown_timer = self.frame_duration
            self.current_frame += 1
            if self.current_frame >= self.sprite.get_num_frames():
                self.current_frame = 0
