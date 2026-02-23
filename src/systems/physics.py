import glm
from entity import get_entity_bounds, get_entity_feet, intersects
from physics.config import GRAVITY
from physics.solver import physics_step

from tiles import TILE_SIZE, collidable_tile_in_list


def zero_accelerations(state):
    for e in state.active_entities:
        e.acc = glm.vec2(0, 0)


def physics_post_step(state):
    physics_step(state)


def gravity(state):
    for e in state.active_entities:
        if e.no_gravity:
            continue
        e.acc.y += GRAVITY


def set_grounded(state):
    # clear grounded
    for e in state.active_entities:
        e.grounded = False

    # find who is grounded
    for e in state.active_entities:
        feet_tl, feet_br = get_entity_feet(e.pos, e.size)

        # check stage floor
        if feet_br.y >= state.stage.wc_dims.y:
            e.grounded = True
            continue

        # get tiles in player feet bounds
        #   # calculate feet position in tile space
        feet_tl_tile_pos = feet_tl / TILE_SIZE
        feet_br_tile_pos = feet_br / TILE_SIZE
        tiles_at_feet = state.stage.get_tiles_in_rect(
            feet_tl_tile_pos, feet_br_tile_pos
        )
        collided = collidable_tile_in_list(tiles_at_feet)
        if collided:
            e.grounded = True

        # get entities in player feet bounds
        for oe in state.active_entities:
            if oe == e:
                continue
            if oe.has_entity_collisions:
                if intersects(feet_tl, feet_br, oe.pos, oe.pos + oe.size):
                    e.grounded = True
