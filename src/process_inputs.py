import pygame

from inputs import PauseInputs, PlayingInputs
from state import Mode


def get_playing_inputs() -> PlayingInputs:
    playing_inputs = PlayingInputs()
    playing_inputs.left = pygame.key.get_pressed()[pygame.K_a]
    playing_inputs.right = pygame.key.get_pressed()[pygame.K_d]
    playing_inputs.up = pygame.key.get_pressed()[pygame.K_w]
    playing_inputs.down = pygame.key.get_pressed()[pygame.K_s]

    playing_inputs.run = pygame.key.get_pressed()[pygame.K_LSHIFT]
    playing_inputs.jump = pygame.key.get_pressed()[pygame.K_SPACE]

    playing_inputs.pause = pygame.key.get_pressed()[pygame.K_RETURN]

    playing_inputs.camera_left = pygame.key.get_pressed()[pygame.K_LEFT]
    playing_inputs.camera_right = pygame.key.get_pressed()[pygame.K_RIGHT]
    playing_inputs.camera_up = pygame.key.get_pressed()[pygame.K_UP]
    playing_inputs.camera_down = pygame.key.get_pressed()[pygame.K_DOWN]

    return playing_inputs


def get_pause_inputs():
    pause_inputs = PauseInputs()
    pause_inputs.pause = pygame.key.get_pressed()[pygame.K_RETURN]
    return pause_inputs


def process_inputs_playing(state):
    state.inputs = get_playing_inputs()


def process_inputs_pause(state):
    state.inputs = get_pause_inputs()


def process_inputs(state):
    match state.mode:
        case Mode.PLAYING:
            process_inputs_playing(state)
        case Mode.PAUSE:
            process_inputs_pause(state)
