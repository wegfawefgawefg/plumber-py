import pygame

from state import Mode
import systems
from systems.control import center_cam_on_player, control_camera, control_entities
from systems.physics import (
    gravity,
    physics_post_step,
    set_grounded,
    zero_accelerations,
)


def step_playing(state, graphics):
    # control_camera(state, graphics)
    zero_accelerations(state)
    gravity(state)
    set_grounded(state)

    control_entities(state)
    physics_post_step(state)

    center_cam_on_player(state, graphics)


def step_pause(state, graphics):
    pass


def step(state, graphics):
    match state.mode:
        case Mode.PLAYING:
            step_playing(state, graphics)
        case Mode.PAUSE:
            step_pause(state, graphics)
