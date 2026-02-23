from physics.config import (
    DEFAULT_ENTITY_WEIGHT,
    ENTITY_DEPENETRATION_ITERATIONS,
    ENTITY_WEIGHTS,
    POSITION_EPSILON,
)
from physics.tile_solver import move_entity_along_axis_against_tiles


def _get_weight(entity):
    if entity.type in ENTITY_WEIGHTS:
        return ENTITY_WEIGHTS[entity.type]
    return DEFAULT_ENTITY_WEIGHT


def _axis_overlap(a, b, axis):
    if axis == "x":
        a_min = a.pos.x
        a_max = a.pos.x + a.size.x
        b_min = b.pos.x
        b_max = b.pos.x + b.size.x
    else:
        a_min = a.pos.y
        a_max = a.pos.y + a.size.y
        b_min = b.pos.y
        b_max = b.pos.y + b.size.y

    return min(a_max, b_max) - max(a_min, b_min)


def _aabb_overlap(a, b):
    ox = _axis_overlap(a, b, "x")
    oy = _axis_overlap(a, b, "y")
    return ox > 0.0 and oy > 0.0


def _axis_separation_directions(a, b, axis):
    if axis == "x":
        a_center = a.pos.x + a.size.x * 0.5
        b_center = b.pos.x + b.size.x * 0.5
    else:
        a_center = a.pos.y + a.size.y * 0.5
        b_center = b.pos.y + b.size.y * 0.5

    if a_center <= b_center:
        return -1.0, 1.0
    return 1.0, -1.0


def _weight_split(a, b):
    w_a = max(_get_weight(a), POSITION_EPSILON)
    w_b = max(_get_weight(b), POSITION_EPSILON)

    inv_a = 1.0 / w_a
    inv_b = 1.0 / w_b
    total = inv_a + inv_b
    if total <= POSITION_EPSILON:
        return 0.5, 0.5
    return inv_a / total, inv_b / total


def resolve_entity_overlaps_on_axis(state, axis):
    collidable = [e for e in state.active_entities if e.has_entity_collisions]
    if len(collidable) < 2:
        return

    for _ in range(ENTITY_DEPENETRATION_ITERATIONS):
        any_overlap = False

        for i in range(len(collidable)):
            for j in range(i + 1, len(collidable)):
                a = collidable[i]
                b = collidable[j]

                if not _aabb_overlap(a, b):
                    continue

                any_overlap = True
                overlap = _axis_overlap(a, b, axis)
                if overlap <= 0.0:
                    continue

                a_dir, b_dir = _axis_separation_directions(a, b, axis)
                a_share, b_share = _weight_split(a, b)
                correction = overlap + POSITION_EPSILON

                a_target = a_dir * correction * a_share
                b_target = b_dir * correction * b_share

                a_moved = a_target
                b_moved = b_target
                if a.has_tile_collisions:
                    a_moved, _ = move_entity_along_axis_against_tiles(
                        state, a, axis, a_target
                    )
                else:
                    if axis == "x":
                        a.pos.x += a_target
                    else:
                        a.pos.y += a_target

                if b.has_tile_collisions:
                    b_moved, _ = move_entity_along_axis_against_tiles(
                        state, b, axis, b_target
                    )
                else:
                    if axis == "x":
                        b.pos.x += b_target
                    else:
                        b.pos.y += b_target

                remaining = _axis_overlap(a, b, axis)
                if remaining > POSITION_EPSILON:
                    fallback = remaining + POSITION_EPSILON
                    if abs(a_target - a_moved) > POSITION_EPSILON:
                        if b.has_tile_collisions:
                            move_entity_along_axis_against_tiles(
                                state, b, axis, b_dir * fallback
                            )
                        else:
                            if axis == "x":
                                b.pos.x += b_dir * fallback
                            else:
                                b.pos.y += b_dir * fallback
                    if abs(b_target - b_moved) > POSITION_EPSILON:
                        if a.has_tile_collisions:
                            move_entity_along_axis_against_tiles(
                                state, a, axis, a_dir * fallback
                            )
                        else:
                            if axis == "x":
                                a.pos.x += a_dir * fallback
                            else:
                                a.pos.y += a_dir * fallback

                if axis == "x":
                    a.vel.x = 0.0
                    b.vel.x = 0.0
                else:
                    a.vel.y = 0.0
                    b.vel.y = 0.0

        if not any_overlap:
            break
