import pygame
import glm
from graphics import Textures

from state import Mode
from tiles import TILE_SIZE, get_tile_texture_sample_position


def render_playing(state, graphics):
    render_tiles(state, graphics)
    render_entites(state, graphics)
    render_ui(state, graphics)


def render_pause(state, graphics):
    pass


def render(state, graphics):
    match state.mode:
        case Mode.PLAYING:
            render_playing(state, graphics)
        case Mode.PAUSE:
            render_pause(state, graphics)


def render_tiles(state, graphics):
    cam = graphics.camera
    tl = cam.pos
    br = cam.pos + cam.size

    tl_tile = tl / TILE_SIZE
    br_tile = br / TILE_SIZE

    tiles_texture = graphics.assets.get(Textures.TILES)
    for y in range(int(tl_tile.y), int(br_tile.y + 2)):
        for x in range(int(tl_tile.x), int(br_tile.x + 1)):
            tile = state.stage.get_tile(x, y)
            if tile is None:
                continue

            sample_pos = get_tile_texture_sample_position(tile) * TILE_SIZE

            render_pos = glm.vec2(x, y) * TILE_SIZE - cam.pos
            graphics.render_surface.blit(
                tiles_texture,
                (render_pos.x, render_pos.y, TILE_SIZE, TILE_SIZE),
                (sample_pos.x, sample_pos.y, TILE_SIZE, TILE_SIZE),
            )


def render_entites(state, graphics):
    cam = graphics.camera
    tl = cam.pos
    br = cam.pos + cam.size

    entities_texture = graphics.assets.get(Textures.ENTITIES)
    for entity in state.entities:
        entity_tl = entity.pos
        entity_br = entity.pos + entity.size

        if entity_br.x < tl.x or entity_tl.x > br.x:
            continue
        if entity_br.y < tl.y or entity_tl.y > br.y:
            continue

        sprite_animator = entity.sprite_animator
        frame_num = sprite_animator.get_current_frame()
        sample_position = sprite_animator.sprite.get_frame_pos(frame_num)
        sample_size = sprite_animator.sprite.get_frame_size(frame_num)
        render_offset = sprite_animator.get_frame_offset()

        render_pos = entity.pos + render_offset - cam.pos

        graphics.render_surface.blit(
            entities_texture,
            (render_pos.x, render_pos.y, entity.size.x, entity.size.y),
            (sample_position.x, sample_position.y, sample_size.x, sample_size.y),
        )


def mouse_pos(graphics):
    return (
        glm.vec2(pygame.mouse.get_pos())
        / graphics.window_size
        * graphics.render_resolution
    )


def render_ui(state, graphics):
    angle = pygame.time.get_ticks() / 1000

    rect_size = glm.vec2(16, 16)
    center = graphics.render_resolution / 2
    rect_pos = center - rect_size / 2 + glm.vec2(32, 32)

    for i in range(3):
        rot = glm.rotate(glm.vec2(0.0, 1.0), angle + i * 90)
        rect_pos_rotated = rot @ (rect_pos - center) + rect_pos
        pygame.draw.rect(
            graphics.render_surface,
            (255, 0, 0),
            (rect_pos_rotated.to_tuple(), rect_size.to_tuple()),
        )

    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mouse_pos(graphics), 10)
