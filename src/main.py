import math
import pygame
import glm
from process_inputs import process_inputs

from render import render
from graphics import Graphics
from stage import STAGE_ONE
from state import State
from audio import Audio
from step import step

pygame.init()


def main():
    state = State()
    graphics = Graphics()
    audio = Audio()

    state.load_stage(STAGE_ONE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        process_inputs(state)
        step(state, graphics)

        graphics.render_surface.fill((0, 0, 0))
        render(state, graphics)
        graphics.blit_render_surface_to_window()

    pygame.quit()


if __name__ == "__main__":
    main()
