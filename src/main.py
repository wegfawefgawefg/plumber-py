import math
from pprint import pprint
import pygame
import glm

from process_inputs import process_inputs
from render import meta_render, render
from graphics import Graphics
from stages.a_a import a_a
from state import State
from audio import Audio, Music, PlaySong
from physics.time_step import FixedStepAccumulator
from step import step

pygame.init()


def main():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    state = State()
    graphics = Graphics()
    audio = Audio()

    state.load_stage(a_a())
    state.snapshot_previous_transforms(graphics)
    audio.events.append(PlaySong(Music.PLAY))

    fixed_step = FixedStepAccumulator()
    clock = pygame.time.Clock()
    running = True
    while running:
        elapsed_seconds = clock.tick(0) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        process_inputs(state)
        fixed_step.add_elapsed(elapsed_seconds)
        simulation_steps = fixed_step.consume_steps()
        for _ in range(simulation_steps):
            step(state, graphics, audio)
        state.render_alpha = fixed_step.alpha()

        graphics.render_surface.fill((0, 0, 0))
        render(state, graphics, state.render_alpha)
        graphics.blit_render_surface_to_window()
        meta_render(state, graphics)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
