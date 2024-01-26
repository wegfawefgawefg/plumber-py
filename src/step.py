import pygame

from state import Mode
from systems.control import control_camera


def step_playing(state, graphics):
    control_camera(state, graphics)


def step_pause(state, graphics):
    pass


def step(state, graphics):
    match state.mode:
        case Mode.PLAYING:
            step_playing(state, graphics)
        case Mode.PAUSE:
            step_pause(state, graphics)
