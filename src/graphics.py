from enum import Enum
import time

import glm
import pygame
from small_ass_cache import AssetCache, loader

from tiles import TILE_SIZE


class Camera:
    def __init__(self, size):
        self.pos = glm.vec2(0, 0)
        self.size = size

    def set_center(self, pos):
        self.pos = pos - self.size / 2

    def get_center(self):
        return self.pos + self.size / 2


class Graphics:
    def __init__(self):
        self.render_resolution = glm.vec2(240, 160) * 1
        self.window_size = self.render_resolution * 4
        self.camera = Camera(glm.vec2(16 * TILE_SIZE, 9 * TILE_SIZE))
        self.camera.set_center(glm.vec2(8 * TILE_SIZE, 10 * TILE_SIZE))

        self.window = pygame.display.set_mode(self.window_size.to_tuple())
        self.render_surface = pygame.Surface(self.render_resolution.to_tuple())

        pygame.display.set_caption("Plumber")

        self.assets = AssetCache()

    def blit_render_surface_to_window(self):
        stretched_surface = pygame.transform.scale(
            self.render_surface, self.window_size
        )
        self.window.blit(stretched_surface, (0, 0))


@loader(pygame.image.load, path="assets/graphics/")
class Textures(Enum):
    ENTITIES = "entities/entities.png"
    TILES = "tiles/land.png"
    DECORATIONS = "decorations/decorations.png"


if __name__ == "__main__":
    graphics = Graphics()

    tiles_texture = graphics.assets.get(Textures.ENTITIES)

    # blit to render texture
    graphics.render_surface.blit(tiles_texture, (0, 0, 100, 100))
    graphics.blit_render_surface_to_window()

    while True:
        pass
