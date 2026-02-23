import math

import glm

from physics.config import POSITION_EPSILON
from tiles import TILE_SIZE, is_tile_collidable


def _aabb_tile_rect(pos, size):
    # Use half-open bounds; subtract epsilon so exact edge alignment doesn't spill to next tile.
    tl = glm.ivec2(
        math.floor(pos.x / TILE_SIZE),
        math.floor(pos.y / TILE_SIZE),
    )
    br = glm.ivec2(
        math.floor((pos.x + size.x - POSITION_EPSILON) / TILE_SIZE),
        math.floor((pos.y + size.y - POSITION_EPSILON) / TILE_SIZE),
    )
    return tl, br


def _colliding_tile_pairs(state, pos, size):
    tl, br = _aabb_tile_rect(pos, size)
    return [
        pair
        for pair in state.stage.get_tile_coord_pairs_in_rect(tl, br)
        if is_tile_collidable(pair.tile)
    ]


def move_entity_along_axis_against_tiles(state, entity, axis, delta):
    if abs(delta) <= POSITION_EPSILON:
        return 0.0, False

    old = glm.vec2(entity.pos)
    next_pos = glm.vec2(entity.pos)
    if axis == "x":
        next_pos.x += delta
    else:
        next_pos.y += delta

    stage_width = state.stage.get_width()
    stage_height = state.stage.get_height()

    if axis == "x":
        next_pos.x = max(0.0, min(next_pos.x, stage_width - entity.size.x))
    else:
        next_pos.y = max(0.0, min(next_pos.y, stage_height - entity.size.y))

    collided = _colliding_tile_pairs(state, next_pos, entity.size)
    if collided:
        if axis == "x":
            if delta > 0:
                left_most = min(pair.coord.x for pair in collided)
                next_pos.x = min(next_pos.x, left_most * TILE_SIZE - entity.size.x)
            else:
                right_most = max(pair.coord.x for pair in collided)
                next_pos.x = max(next_pos.x, (right_most + 1) * TILE_SIZE)
        else:
            if delta > 0:
                top_most = min(pair.coord.y for pair in collided)
                next_pos.y = min(next_pos.y, top_most * TILE_SIZE - entity.size.y)
            else:
                bottom_most = max(pair.coord.y for pair in collided)
                next_pos.y = max(next_pos.y, (bottom_most + 1) * TILE_SIZE)

    actual = next_pos - old
    blocked = abs((actual.x if axis == "x" else actual.y) - delta) > POSITION_EPSILON
    entity.pos = next_pos
    return actual.x if axis == "x" else actual.y, blocked
