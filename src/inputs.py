import pygame
import glm


class PlayingInputs:
    def __init__(self) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.run = False
        self.jump = False

        self.pause = False

        self.camera_left = False
        self.camera_right = False
        self.camera_up = False
        self.camera_down = False


class PauseInputs:
    def __init__(self) -> None:
        self.pause = False
