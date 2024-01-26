import pygame

from state import Mode
import systems
from systems.control import center_cam_on_player, control_camera, control_entities
from systems.physics import physics_post_step, physics_pre_step, physics_step


def step_playing(state, graphics):
    # control_camera(state, graphics)
    physics_pre_step(state)

    control_entities(state)
    physics_step(state)
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
