import math

from physics.config import (
    MAX_MOTION_PER_SUBSTEP,
    MAX_SPEED,
    MAX_SUBSTEPS_PER_TICK,
    MIN_SUBSTEPS_PER_TICK,
)
from physics.contact import reset_entity_contact_summaries
from physics.entity_solver import resolve_entity_overlaps_on_axis
from physics.tile_solver import move_entity_along_axis_against_tiles


def _integrate_velocities(state):
    for entity in state.active_entities:
        entity.vel += entity.acc

        if entity.vel.x > MAX_SPEED:
            entity.vel.x = MAX_SPEED
        elif entity.vel.x < -MAX_SPEED:
            entity.vel.x = -MAX_SPEED

        if entity.vel.y > MAX_SPEED:
            entity.vel.y = MAX_SPEED
        elif entity.vel.y < -MAX_SPEED:
            entity.vel.y = -MAX_SPEED


def _substeps_for_tick(state):
    max_motion = 0.0
    for entity in state.active_entities:
        max_motion = max(max_motion, abs(entity.vel.x), abs(entity.vel.y))

    if max_motion <= 0.0:
        return MIN_SUBSTEPS_PER_TICK

    steps = math.ceil(max_motion / MAX_MOTION_PER_SUBSTEP)
    steps = max(MIN_SUBSTEPS_PER_TICK, min(steps, MAX_SUBSTEPS_PER_TICK))
    return int(steps)


def _move_axis(state, axis, substeps):
    for entity in state.active_entities:
        delta = (entity.vel.x / substeps) if axis == "x" else (entity.vel.y / substeps)

        if not (entity.has_tile_collisions or entity.has_entity_collisions):
            if axis == "x":
                entity.pos.x += delta
            else:
                entity.pos.y += delta
            continue

        blocked_by_tiles = False
        if entity.has_tile_collisions:
            _, blocked_by_tiles = move_entity_along_axis_against_tiles(
                state,
                entity,
                axis,
                delta,
            )
        else:
            if axis == "x":
                entity.pos.x += delta
            else:
                entity.pos.y += delta

        if blocked_by_tiles:
            if axis == "x":
                entity.vel.x = 0.0
            else:
                entity.vel.y = 0.0


# Fixed-tick simulation step.
def physics_step(state):
    reset_entity_contact_summaries(state)
    _integrate_velocities(state)

    substeps = _substeps_for_tick(state)
    for _ in range(substeps):
        _move_axis(state, "x", substeps)
        resolve_entity_overlaps_on_axis(state, "x")

        _move_axis(state, "y", substeps)
        resolve_entity_overlaps_on_axis(state, "y")
