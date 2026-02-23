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
    audio.events.append(PlaySong(Music.PLAY))

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
        step(state, graphics, audio)

        graphics.render_surface.fill((0, 0, 0))
        render(state, graphics)
        graphics.blit_render_surface_to_window()
        meta_render(state, graphics)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
