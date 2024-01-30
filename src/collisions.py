import pygame
from glm import ceil, floor, vec2, ivec2
from entity import Entity, get_entity_bounds, intersects
from events import Side
from state import State

from tiles import TILE_SIZE, is_tile_collidable
from events import EntityTileCollision


class TileCoordPair:
    def __init__(self, tile, coord):
        self.tile = tile
        self.coord = coord


class EntityTileCollision:
    def __init__(self, entity, tile, tile_coord, side, pos, vel):
        self.entity: Entity = entity
        self.tile = tile
        self.tile_coord = tile_coord
        self.side: Side = side
        self.pos = pos
        self.vel = vel

    def __repr__(self) -> str:
        return f"ETC({self.entity}, {self.tile}, {self.side}, ({self.pos.x:.2f}, {self.pos.y:.2f}), ({self.vel.x:.2f}, {self.vel.y:.2f}))"


class EntityEntityCollision:
    def __init__(self, entity_a, entity_b, side, pos, vel):
        self.entity_a = entity_a
        self.entity_b = entity_b
        self.side = side
        self.pos = pos
        self.vel = vel

    def __repr__(self) -> str:
        return f"EEC({self.entity_a}, {self.entity_b}, {self.side}, ({self.pos.x:.2f}, {self.pos.y:.2f}), ({self.vel.x:.2f}, {self.vel.y:.2f}))"


def do_collisions_vertical(
    state: State, entity, pos: ivec2, size: ivec2, vel: vec2
) -> None | float:
    """Returns the new y position if collided, False otherwise"""
    stage = state.stage

    y_vel = vel.y
    if y_vel > 0:
        y_vel = ceil(y_vel)
    elif y_vel < 0:
        y_vel = floor(y_vel)

    one_dim_vel = vec2(0, y_vel)
    next_pos = pos + one_dim_vel
    next_pos_tl = next_pos
    next_pos_br = next_pos + size - vec2(1, 1)

    # Check if out of bounds in y direction
    if next_pos_tl.y < 0:
        return 0.0
    elif next_pos_br.y > stage.get_height() - 1:
        return stage.get_height() - size.y

    # Check for collisions with tiles
    np_tl_tile_pos = ivec2(next_pos_tl) // ivec2(TILE_SIZE, TILE_SIZE)
    np_br_tile_pos = ivec2(next_pos_br) // ivec2(TILE_SIZE, TILE_SIZE)

    intersected_tile_coord_pairs = stage.get_tile_coord_pairs_in_rect(
        np_tl_tile_pos, np_br_tile_pos
    )
    collided_tile_coord_pairs = [
        tcp for tcp in intersected_tile_coord_pairs if is_tile_collidable(tcp.tile)
    ]

    if collided_tile_coord_pairs:  # collided
        if vel.y > 0.0:
            top_most_tile_y = min(tcp.coord.y for tcp in collided_tile_coord_pairs)
            top_most_y = top_most_tile_y * TILE_SIZE
            new_y_pos = top_most_y - size.y

            # trigger events
            top_most_tile_coord_pairs = [
                tcp
                for tcp in collided_tile_coord_pairs
                if tcp.coord.y == top_most_tile_y
            ]
            for tcp in top_most_tile_coord_pairs:
                state.events.append(
                    EntityTileCollision(
                        entity, tcp.tile, tcp.coord, Side.BOTTOM, pos, vel
                    )
                )

            return new_y_pos

        elif vel.y < 0.0:
            bottom_most_tile_y = max(tcp.coord.y for tcp in collided_tile_coord_pairs)
            bottom_most_y = (bottom_most_tile_y + 1) * TILE_SIZE
            new_y_pos = bottom_most_y

            # trigger events
            bottom_most_tile_coord_pairs = [
                tcp
                for tcp in collided_tile_coord_pairs
                if tcp.coord.y == bottom_most_tile_y
            ]
            for tcp in bottom_most_tile_coord_pairs:
                state.events.append(
                    EntityTileCollision(entity, tcp.tile, tcp.coord, Side.TOP, pos, vel)
                )

            return new_y_pos

    return None


def do_collisions_horizontal(
    state: State, entity, pos: ivec2, size: ivec2, vel: vec2
) -> None | float:
    """Returns the new x position if collided, False otherwise"""
    stage = state.stage

    x_vel = vel.x
    if x_vel > 0:
        x_vel = ceil(x_vel)
    elif x_vel < 0:
        x_vel = floor(x_vel)

    one_dim_vel = vec2(x_vel, 0)
    next_pos = pos + one_dim_vel
    next_pos_tl = next_pos
    next_pos_br = next_pos + size - vec2(1, 1)

    # Check if out of bounds in x direction
    if next_pos_tl.x < 0:
        return 0.0
    elif next_pos_br.x > stage.get_width() - 1:
        return stage.get_width() - size.x

    # Check for collisions with tiles
    np_tl_tile_pos = ivec2(next_pos_tl) // ivec2(TILE_SIZE, TILE_SIZE)
    np_br_tile_pos = ivec2(next_pos_br) // ivec2(TILE_SIZE, TILE_SIZE)

    intersected_tile_coord_pairs = stage.get_tile_coord_pairs_in_rect(
        np_tl_tile_pos, np_br_tile_pos
    )
    collided_tile_coord_pairs = [
        tcp for tcp in intersected_tile_coord_pairs if is_tile_collidable(tcp.tile)
    ]

    if collided_tile_coord_pairs:  # collided
        if vel.x > 0.0:
            left_most_tile_x = min(tcp.coord.x for tcp in collided_tile_coord_pairs)
            left_most_x = left_most_tile_x * TILE_SIZE
            new_x_pos = left_most_x - size.x

            # trigger events
            left_most_tile_coord_pairs = [
                tcp
                for tcp in collided_tile_coord_pairs
                if tcp.coord.x == left_most_tile_x
            ]
            for tcp in left_most_tile_coord_pairs:
                state.events.append(
                    EntityTileCollision(
                        entity, tcp.tile, tcp.coord, Side.LEFT, pos, vel
                    )
                )

            return new_x_pos

        elif vel.x < 0.0:
            right_most_tile_x = max(tcp.coord.x for tcp in collided_tile_coord_pairs)
            right_most_x = (right_most_tile_x + 1) * TILE_SIZE
            new_x_pos = right_most_x

            # trigger events
            right_most_tile_coord_pairs = [
                tcp
                for tcp in collided_tile_coord_pairs
                if tcp.coord.x == right_most_tile_x
            ]
            for tcp in right_most_tile_coord_pairs:
                state.events.append(
                    EntityTileCollision(
                        entity, tcp.tile, tcp.coord, Side.RIGHT, pos, vel
                    )
                )

            return new_x_pos
    return None


def do_entity_collisions_vertical(
    state: State, entity, pos: ivec2, size: ivec2, vel: vec2
) -> None | float:
    """Returns the new y position if collided, False otherwise"""
    stage = state.stage

    y_vel = vel.y
    if y_vel > 0:
        y_vel = ceil(y_vel)
    elif y_vel < 0:
        y_vel = floor(y_vel)

    one_dim_vel = vec2(0, y_vel)
    next_pos = pos + one_dim_vel
    next_pos_tl = next_pos
    next_pos_br = next_pos + size - vec2(1, 1)

    # find intersected entities
    intersected_entities = []
    for oe in state.active_entities:
        if oe == entity:
            continue
        oe_tl, oe_br = get_entity_bounds(oe.pos, oe.size)
        if intersects(next_pos_tl, next_pos_br, oe_tl, oe_br):
            intersected_entities.append(oe)

    collided_entities = [oe for oe in intersected_entities if oe.has_entity_collisions]

    if collided_entities:  # collided
        if vel.y > 0.0:
            top_most_y = min(oe.pos.y for oe in collided_entities)
            new_y_pos = top_most_y - size.y

            # trigger events
            top_most_entities = [
                oe for oe in collided_entities if oe.pos.y == top_most_y
            ]
            for oe in top_most_entities:
                state.events.append(
                    EntityEntityCollision(entity, oe, Side.BOTTOM, pos, vel)
                )

            return new_y_pos

        elif vel.y < 0.0:
            bottom_most_y = max(oe.pos.y + oe.size.y for oe in collided_entities)
            new_y_pos = bottom_most_y

            # trigger events
            bottom_most_entities = [
                oe for oe in collided_entities if oe.pos.y == bottom_most_y
            ]
            for oe in bottom_most_entities:
                state.events.append(
                    EntityEntityCollision(entity, oe, Side.TOP, pos, vel)
                )

            return new_y_pos

    return None


def do_entity_collisions_horizontal(
    state: State, entity, pos: ivec2, size: ivec2, vel: vec2
) -> None | float:
    """Returns the new x position if collided, None otherwise"""
    stage = state.stage

    x_vel = vel.x
    if x_vel > 0:
        x_vel = ceil(x_vel)
    elif x_vel < 0:
        x_vel = floor(x_vel)

    one_dim_vel = vec2(x_vel, 0)
    next_pos = pos + one_dim_vel
    next_pos_tl = next_pos
    next_pos_br = next_pos + size - vec2(1, 1)

    # find intersected entities
    intersected_entities = []
    for oe in state.active_entities:
        if oe == entity:
            continue
        oe_tl, oe_br = get_entity_bounds(oe.pos, oe.size)
        if intersects(next_pos_tl, next_pos_br, oe_tl, oe_br):
            intersected_entities.append(oe)

    collided_entities = [oe for oe in intersected_entities if oe.has_entity_collisions]

    if collided_entities:  # collided
        if vel.x > 0.0:
            left_most_x = min(oe.pos.x for oe in collided_entities)
            new_x_pos = left_most_x - size.x

            # trigger events
            left_most_entities = [
                oe for oe in collided_entities if oe.pos.x == left_most_x
            ]
            for oe in left_most_entities:
                state.events.append(
                    EntityEntityCollision(entity, oe, Side.RIGHT, pos, vel)
                )

            return new_x_pos

        elif vel.x < 0.0:
            right_most_x = max(oe.pos.x + oe.size.x for oe in collided_entities)
            new_x_pos = right_most_x

            # trigger events
            right_most_entities = [
                oe for oe in collided_entities if oe.pos.x == right_most_x
            ]
            for oe in right_most_entities:
                state.events.append(
                    EntityEntityCollision(entity, oe, Side.LEFT, pos, vel)
                )

            return new_x_pos

    return None
