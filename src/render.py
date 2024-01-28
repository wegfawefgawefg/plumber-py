import pygame
import glm
from entity import Facing
from graphics import Textures

from state import Mode
from tiles import TILE_SIZE, get_tile_texture_sample_position, is_tile_transparent


def render_playing(state, graphics):
    render_tiles(state, graphics)
    render_background_decorations(state, graphics)
    # render_crosshair(state, graphics)
    render_entites(state, graphics)
    render_foreground_decorations(state, graphics)
    render_alerts(state, graphics)
    render_ui(state, graphics)


def render_crosshair(state, graphics):
    # draw a line down the middle of the screen
    pygame.draw.line(
        graphics.render_surface,
        (255, 0, 0),
        (graphics.render_resolution.x / 2, 0),
        (graphics.render_resolution.x / 2, graphics.render_resolution.y),
    )

    # now horizontally
    pygame.draw.line(
        graphics.render_surface,
        (255, 0, 0),
        (0, graphics.render_resolution.y / 2),
        (graphics.render_resolution.x, graphics.render_resolution.y / 2),
    )


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
    br = tl + cam.size

    tl_tile = tl // TILE_SIZE
    br_tile = br // TILE_SIZE

    tiles_texture = graphics.assets.get(Textures.TILES)
    for y in range(int(tl_tile.y), int(br_tile.y + 2)):
        for x in range(int(tl_tile.x), int(br_tile.x + 1)):
            tile = state.stage.get_tile(x, y)
            if tile is None:
                continue

            sample_pos = get_tile_texture_sample_position(tile) * TILE_SIZE

            render_pos = glm.vec2(x, y) * TILE_SIZE - cam.pos
            # if tile is transparent, render an air beneath it
            if is_tile_transparent(tile):
                graphics.render_surface.blit(
                    tiles_texture,
                    (render_pos.x, render_pos.y, TILE_SIZE, TILE_SIZE),
                    (0, 0, TILE_SIZE, TILE_SIZE),
                )
            graphics.render_surface.blit(
                tiles_texture,
                (render_pos.x, render_pos.y, TILE_SIZE, TILE_SIZE),
                (sample_pos.x, sample_pos.y, TILE_SIZE, TILE_SIZE),
            )


def render_background_decorations(state, graphics):
    render_decorations(state, graphics, state.stage.background_decorations)


def render_foreground_decorations(state, graphics):
    render_decorations(state, graphics, state.stage.foreground_decorations)


def render_decorations(state, graphics, decorations):
    cam = graphics.camera
    tl = cam.pos
    br = tl + cam.size

    decorations_texture = graphics.assets.get(Textures.DECORATIONS)
    for decoration in decorations:
        sprite_animator = decoration.sprite_animator
        frame_num = sprite_animator.get_current_frame()
        sample_pos = sprite_animator.sprite.get_frame_pos(frame_num)
        sample_size = sprite_animator.sprite.get_frame_size(frame_num)
        render_offset = sprite_animator.get_frame_offset()

        decoration_tl = decoration.pos
        decoration_br = decoration.pos + sample_size

        if decoration_br.x < tl.x or decoration_tl.x > br.x:
            continue
        if decoration_br.y < tl.y or decoration_tl.y > br.y:
            continue

        render_pos = decoration.pos + render_offset - cam.pos

        graphics.render_surface.blit(
            decorations_texture,
            (render_pos.x, render_pos.y, sample_size.x, sample_size.y),
            (sample_pos.x, sample_pos.y, sample_size.x, sample_size.y),
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

        # render the entity box
        # pygame.draw.rect(
        #     graphics.render_surface,
        #     (255, 0, 0),
        #     (
        #         entity.pos.x - cam.pos.x,
        #         entity.pos.y - cam.pos.y,
        #         entity.size.x,
        #         entity.size.y,
        #     ),
        #     1,
        # )

        sprite_animator = entity.sprite_animator
        frame_num = sprite_animator.get_current_frame()
        sample_position = sprite_animator.sprite.get_frame_pos(frame_num)
        sample_size = sprite_animator.sprite.get_frame_size(frame_num)
        render_offset = sprite_animator.get_frame_offset()

        # sample the entity texture into a surface
        sample_surface = pygame.Surface(sample_size.to_tuple(), pygame.SRCALPHA)
        sample_surface.blit(
            entities_texture,
            (0, 0, sample_size.x, sample_size.y),
            (sample_position.x, sample_position.y, sample_size.x, sample_size.y),
        )
        # flip the surface if the entity is facing right
        if entity.facing == Facing.RIGHT:
            sample_surface = pygame.transform.flip(sample_surface, True, False)
            # invert render offset

            render_pos = entity.pos + render_offset - cam.pos
            render_offset = glm.vec2(render_offset.x, render_offset.y)

        render_pos = entity.pos + render_offset - cam.pos

        # blit the surface to the render surface
        graphics.render_surface.blit(
            sample_surface,
            (render_pos.x, render_pos.y, sample_size.x, sample_size.y),
        )

    # render a fake entity as the origin line
    origin_tile_pos = glm.vec2(0, 12)
    origin_pos = origin_tile_pos * TILE_SIZE - cam.pos
    pygame.draw.line(
        graphics.render_surface,
        (0, 255, 0),
        (origin_pos.x, origin_pos.y),
        (origin_pos.x + 8, origin_pos.y),
    )
    pygame.draw.line(
        graphics.render_surface,
        (0, 255, 0),
        (origin_pos.x, origin_pos.y),
        (origin_pos.x, origin_pos.y + 8),
    )


def mouse_pos(graphics):
    return (
        glm.vec2(pygame.mouse.get_pos())
        / graphics.window_size
        * graphics.render_resolution
    )


def render_ui(state, graphics):
    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mouse_pos(graphics), 3)


def meta_render(state, graphics):
    # render_debug_messages(state, graphics)
    pass


def render_debug_messages(state, graphics):
    state.debug_messages.sort()

    cursor = glm.vec2(0, 0)
    for string in state.debug_messages:
        text = string
        color = (255, 255, 255)
        font = pygame.font.SysFont("Arial", 16)

        font_surface = font.render(text, True, color)
        graphics.window.blit(font_surface, cursor.to_tuple())

        cursor.y += font.get_height()


def render_alerts(state, graphics):
    # sort by the lifetime
    state.alerts.sort(
        key=lambda alert: alert.lifetime,
        reverse=True,
    )

    # half width
    half_width = graphics.render_resolution.x / 2
    cursor = glm.vec2(half_width, 0)
    for alert in state.alerts:
        text = alert.text
        color = (255, 255, 255)
        font = pygame.font.SysFont("Arial", 12)

        font_surface = font.render(text, True, color)
        graphics.render_surface.blit(font_surface, cursor.to_tuple())

        cursor.y += font.get_height()
