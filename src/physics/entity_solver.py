import math
from collections import defaultdict

from physics.config import (
    ENTITY_BROADPHASE_CELL_SIZE,
    POSITION_EPSILON,
)
from physics.contact import register_entity_contact
from physics.tile_solver import move_entity_along_axis_against_tiles


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


def _zero_velocity_into_entity_contact(axis, entity, separation_dir):
    if axis == "y":
        # If depenetration moved the body up, it was penetrating from above
        # (falling into the other body); if moved down, it was penetrating from below.
        if separation_dir < 0.0 and entity.vel.y > 0.0:
            entity.vel.y = 0.0
        elif separation_dir > 0.0 and entity.vel.y < 0.0:
            entity.vel.y = 0.0


def _entities_should_collide(a, b):
    # Explicit push policy: resolve only pairs where one side can push and
    # the other side can be pushed.
    return (a.can_push_entities and b.can_be_pushed) or (
        b.can_push_entities and a.can_be_pushed
    )


def _full_displacement_targets(axis, a, b, overlap, a_dir, b_dir):
    a_pushes_b = a.can_push_entities and b.can_be_pushed
    b_pushes_a = b.can_push_entities and a.can_be_pushed

    if a_pushes_b and not b_pushes_a:
        return 0.0, b_dir * overlap, a, b, a_dir
    if b_pushes_a and not a_pushes_b:
        return a_dir * overlap, 0.0, b, a, b_dir

    # If both can push each other, choose a single pusher by larger axis speed.
    a_axis_speed = abs(a.vel.x) if axis == "x" else abs(a.vel.y)
    b_axis_speed = abs(b.vel.x) if axis == "x" else abs(b.vel.y)
    if a_axis_speed >= b_axis_speed:
        return 0.0, b_dir * overlap, a, b, a_dir
    return a_dir * overlap, 0.0, b, a, b_dir


def _crush_entity(entity):
    entity.hp = 0
    entity.ai = None
    entity.vel.x = 0.0
    entity.vel.y = 0.0
    entity.acc.x = 0.0
    entity.acc.y = 0.0
    entity.has_entity_collisions = False
    entity.can_push_entities = False
    entity.can_be_pushed = False


def _can_crush_in_direction(pusher, axis, pushee_target):
    if axis == "x":
        if pushee_target > POSITION_EPSILON:
            return pusher.can_crush_right
        if pushee_target < -POSITION_EPSILON:
            return pusher.can_crush_left
        return False

    if pushee_target > POSITION_EPSILON:
        return pusher.can_crush_down
    if pushee_target < -POSITION_EPSILON:
        return pusher.can_crush_up
    return False


def _candidate_pair_indices(collidable):
    buckets = defaultdict(list)
    cell_size = ENTITY_BROADPHASE_CELL_SIZE

    for index, entity in enumerate(collidable):
        min_x = int(math.floor(entity.pos.x / cell_size))
        max_x = int(
            math.floor((entity.pos.x + entity.size.x - POSITION_EPSILON) / cell_size)
        )
        min_y = int(math.floor(entity.pos.y / cell_size))
        max_y = int(
            math.floor((entity.pos.y + entity.size.y - POSITION_EPSILON) / cell_size)
        )

        for cy in range(min_y, max_y + 1):
            for cx in range(min_x, max_x + 1):
                buckets[(cx, cy)].append(index)

    pairs = set()
    for indices in buckets.values():
        if len(indices) < 2:
            continue
        for a_i in range(len(indices) - 1):
            i = indices[a_i]
            for b_i in range(a_i + 1, len(indices)):
                j = indices[b_i]
                if i == j:
                    continue
                if i < j:
                    pairs.add((i, j))
                else:
                    pairs.add((j, i))

    return sorted(
        (i, j)
        for i, j in pairs
        if _entities_should_collide(collidable[i], collidable[j])
    )


def resolve_entity_overlaps_on_axis(state, axis):
    collidable = [e for e in state.active_entities if e.has_entity_collisions]
    if len(collidable) < 2:
        return

    # Full-displacement policy resolves each overlap in one pass.
    for _ in range(1):
        any_overlap = False
        pair_indices = _candidate_pair_indices(collidable)
        if not pair_indices:
            break

        for i, j in pair_indices:
            a = collidable[i]
            b = collidable[j]

            ox = _axis_overlap(a, b, "x")
            oy = _axis_overlap(a, b, "y")
            if ox <= 0.0 or oy <= 0.0:
                continue

            if axis == "x":
                if ox > oy + POSITION_EPSILON:
                    continue
                overlap = ox
            else:
                if oy > ox + POSITION_EPSILON:
                    continue
                overlap = oy

            any_overlap = True

            a_dir, b_dir = _axis_separation_directions(a, b, axis)
            register_entity_contact(state, a, b, axis, a_dir, b_dir)
            a_target, b_target, pusher, pushee, pusher_dir = _full_displacement_targets(
                axis, a, b, overlap, a_dir, b_dir
            )

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

            a_blocked = abs(a_target - a_moved) > POSITION_EPSILON
            b_blocked = abs(b_target - b_moved) > POSITION_EPSILON
            pushee_blocked = (pushee is a and a_blocked) or (pushee is b and b_blocked)
            pushee_target = a_target if pushee is a else b_target

            if pushee_blocked:
                if pushee.can_be_squished and _can_crush_in_direction(
                    pusher, axis, pushee_target
                ):
                    _crush_entity(pushee)
                    continue

                remaining = _axis_overlap(a, b, axis)
                if remaining > POSITION_EPSILON:
                    reject_delta = pusher_dir * remaining
                    if pusher.has_tile_collisions:
                        move_entity_along_axis_against_tiles(
                            state, pusher, axis, reject_delta
                        )
                    else:
                        if axis == "x":
                            pusher.pos.x += reject_delta
                        else:
                            pusher.pos.y += reject_delta

                if axis == "x":
                    pusher.vel.x = 0.0
                else:
                    pusher.vel.y = 0.0

            # Preserve horizontal momentum for entity-entity contacts to keep
            # pushing behavior natural. Vertical velocity is still canceled
            # when penetrating into another body so gravity doesn't accumulate
            # while standing on moving entities.
            _zero_velocity_into_entity_contact(axis, a, a_dir)
            _zero_velocity_into_entity_contact(axis, b, b_dir)

            # Still kill axis velocity when depenetration against tiles blocks
            # the intended correction.
            a_tile_blocked = a_blocked
            b_tile_blocked = b_blocked
            if axis == "x":
                if a_tile_blocked:
                    a.vel.x = 0.0
                if b_tile_blocked:
                    b.vel.x = 0.0
            else:
                if a_tile_blocked:
                    a.vel.y = 0.0
                if b_tile_blocked:
                    b.vel.y = 0.0

        if not any_overlap:
            break
