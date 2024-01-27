import math
import pygame
import glm
from process_inputs import process_inputs

from render import meta_render, render, render_debug_messages
from graphics import Graphics
from stages.a_a import a_a
from state import State
from audio import Audio
from step import step

pygame.init()


def main():
    state = State()
    graphics = Graphics()
    audio = Audio()

    state.load_stage(a_a())

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        process_inputs(state)
        state.meta_step()
        step(state, graphics)

        graphics.render_surface.fill((0, 0, 0))
        render(state, graphics)
        graphics.blit_render_surface_to_window()
        meta_render(state, graphics)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
