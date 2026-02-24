from math import ceil
import pygame
import glm
from entity import EntityType, Facing, get_entity_feet
from graphics import Textures

from state import Mode
from tiles import TILE_SIZE, get_tile_texture_sample_position, is_tile_transparent

DEBUG_RENDER_ENTITY_AABBS = True


def _lerp_vec2(a, b, alpha):
    return a + (b - a) * alpha


def _camera_pos(graphics, alpha):
    return _lerp_vec2(graphics.camera.prev_pos, graphics.camera.pos, alpha)


def _entity_render_pos(entity, alpha):
    return _lerp_vec2(entity.prev_pos, entity.pos, alpha)


def render_playing(state, graphics, alpha):
    render_tiles(state, graphics, alpha)
    render_background_decorations(state, graphics, alpha)
    # render_crosshair(state, graphics)
    render_entites(state, graphics, alpha)
    render_foreground_decorations(state, graphics, alpha)
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


def render(state, graphics, alpha=1.0):
    match state.mode:
        case Mode.PLAYING:
            render_playing(state, graphics, alpha)
        case Mode.PAUSE:
            render_pause(state, graphics)


def render_tiles(state, graphics, alpha):
    cam = graphics.camera
    cam_pos = _camera_pos(graphics, alpha)
    tl = cam_pos
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

            render_pos = glm.vec2(x, y) * TILE_SIZE - cam_pos
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


def render_background_decorations(state, graphics, alpha):
    render_decorations(
        state, graphics, state.stage.background_decorations, alpha, tint=True
    )


def render_foreground_decorations(state, graphics, alpha):
    render_decorations(state, graphics, state.stage.foreground_decorations, alpha)


def render_decorations(state, graphics, decorations, alpha, tint=False):
    cam = graphics.camera
    cam_pos = _camera_pos(graphics, alpha)
    tl = cam_pos
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

        decoration_surface = pygame.Surface(sample_size.to_tuple(), pygame.SRCALPHA)
        decoration_surface.blit(
            decorations_texture,
            (0, 0, sample_size.x, sample_size.y),
            (sample_pos.x, sample_pos.y, sample_size.x, sample_size.y),
        )
        if tint:
            ckeep = 0
            alpha = 200
            decoration_surface.fill(
                (ckeep, ckeep, ckeep, alpha), None, pygame.BLEND_RGBA_MULT
            )
        if decoration.flip:
            decoration_surface = pygame.transform.flip(decoration_surface, True, False)
        render_pos = decoration.pos + render_offset - cam_pos

        graphics.render_surface.blit(
            decoration_surface,
            (render_pos.x, render_pos.y, sample_size.x, sample_size.y),
            (0, 0, sample_size.x, sample_size.y),
        )


def render_entites(state, graphics, alpha):
    cam = graphics.camera
    cam_pos = _camera_pos(graphics, alpha)
    tl = cam_pos
    br = cam_pos + cam.size

    entities_texture = graphics.assets.get(Textures.ENTITIES)
    for entity in state.entities:
        entity_pos = _entity_render_pos(entity, alpha)
        entity_tl = entity_pos
        entity_br = entity_pos + entity.size

        if entity_br.x < tl.x or entity_tl.x > br.x:
            continue
        if entity_br.y < tl.y or entity_tl.y > br.y:
            continue

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

            # a width of 5 would be a single tile wide
            # a width of 17 would be 2 tiles wide
            num_tiles_wide = ceil(sample_size.x / TILE_SIZE)
            area_width = num_tiles_wide * TILE_SIZE

            # maybe BUG: sprites may need to store their sample width, not just the sprite area widths
            flipped_offset = -abs(area_width + render_offset.x - entity.size.x)
            render_offset = glm.vec2(flipped_offset, render_offset.y)
        render_pos = entity_pos + render_offset - cam_pos

        # blit the surface to the render surface
        graphics.render_surface.blit(
            sample_surface,
            (render_pos.x, render_pos.y, sample_size.x, sample_size.y),
        )

        if DEBUG_RENDER_ENTITY_AABBS:
            pygame.draw.rect(
                graphics.render_surface,
                (255, 0, 0),
                (
                    int(entity_pos.x - cam_pos.x),
                    int(entity_pos.y - cam_pos.y),
                    int(entity.size.x),
                    int(entity.size.y),
                ),
                1,
            )

        # draw entity feet
        # feet_tl, feet_br = get_entity_feet(entity.pos, entity.size)
        # state.debug_messages.append(f"pos: {entity.pos}")
        # state.debug_messages.append(f"feet: {feet_tl} {feet_br}")
        # feet_tl = glm.vec2(feet_tl.x, feet_tl.y) - cam.pos
        # feet_br = glm.vec2(feet_br.x, feet_br.y) - cam.pos
        # # draw rect
        # pygame.draw.rect(
        #     graphics.render_surface,
        #     (0, 255, 0),
        #     (
        #         feet_tl.x,
        #         feet_tl.y,
        #         feet_br.x - feet_tl.x,
        #         feet_br.y - feet_tl.y,
        #     ),
        #     1,
        # )

    # render a fake entity as the origin line
    # origin_tile_pos = glm.vec2(0, 12)
    # origin_pos = origin_tile_pos * TILE_SIZE - cam.pos
    # pygame.draw.line(
    #     graphics.render_surface,
    #     (0, 255, 0),
    #     (origin_pos.x, origin_pos.y),
    #     (origin_pos.x + 8, origin_pos.y),
    # )
    # pygame.draw.line(
    #     graphics.render_surface,
    #     (0, 255, 0),
    #     (origin_pos.x, origin_pos.y),
    #     (origin_pos.x, origin_pos.y + 8),
    # )


def mouse_pos(graphics):
    return (
        glm.vec2(pygame.mouse.get_pos())
        / graphics.window_size
        * graphics.render_resolution
    )


def render_ui(state, graphics):
    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mouse_pos(graphics), 3)


def meta_render(state, graphics):
    debug_bottom = render_debug_messages(state, graphics)
    render_alerts(state, graphics, start_y=debug_bottom + 8)


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
    return cursor.y


def render_alerts(state, graphics, start_y=0):
    # sort by the lifetime
    state.alerts.sort(
        key=lambda alert: alert.lifetime,
        reverse=True,
    )

    cursor = glm.vec2(12, start_y)
    for alert in state.alerts:
        text = alert.text
        color = getattr(alert, "color", (255, 255, 255))
        font = pygame.font.SysFont("Arial", 18)

        font_surface = font.render(text, True, color)
        graphics.window.blit(font_surface, cursor.to_tuple())

        cursor.y += font.get_height()
