import glm
from collisions import (
    do_collisions_horizontal,
    do_collisions_vertical,
)
from entity import get_entity_bounds

from tiles import TILE_SIZE, collidable_tile_in_list


def zero_accelerations(state):
    for e in state.entities:
        e.acc = glm.vec2(0, 0)


MAX_SPEED = 9.0


def ground_friction(state):
    for e in state.entities:
        if e.grounded:
            e.vel.x *= 0.8


def physics_post_step(state):
    for e in state.entities:
        e.vel += e.acc

        # clamp
        if e.vel.x > MAX_SPEED:
            e.vel.x = MAX_SPEED
        elif e.vel.x < -MAX_SPEED:
            e.vel.x = -MAX_SPEED
        if e.vel.y > MAX_SPEED:
            e.vel.y = MAX_SPEED
        elif e.vel.y < -MAX_SPEED:
            e.vel.y = -MAX_SPEED

        # collisions
        #   # horizontal
        new_pos = do_collisions_vertical(state, e, e.pos, e.size, e.vel)
        if new_pos != None:
            e.pos.y = new_pos
            e.vel.y = 0.0
        else:
            e.pos.y += e.vel.y

        #   # horizontal
        new_pos = do_collisions_horizontal(state, e, e.pos, e.size, e.vel)
        if new_pos != None:
            e.pos.x = new_pos
            e.vel.x = 0.0
        else:
            e.pos.x += e.vel.x


GRAVITY = 0.3


def gravity(state):
    for e in state.entities:
        if e.no_gravity:
            continue
        e.acc.y += GRAVITY


def set_grounded(state):
    # clear grounded
    for e in state.entities:
        e.grounded = False

    # find who is grounded
    for e in state.entities:
        entity_tl, entity_br = get_entity_bounds(e.pos, e.size)

        feet_tl = glm.vec2(entity_tl.x, entity_br.y)
        feet_br = entity_br + glm.vec2(0, 1)

        # check stage floor
        if feet_br.y >= state.stage.wc_dims.y:
            e.grounded = True
            continue

        # get tiles in player bounds
        feet_tl_tile_pos = feet_tl / TILE_SIZE
        feet_br_tile_pos = feet_br / TILE_SIZE
        tiles_at_feet = state.stage.get_tiles_in_rect(
            feet_tl_tile_pos, feet_br_tile_pos
        )
        collided = collidable_tile_in_list(tiles_at_feet)
        if collided:
            e.grounded = True
            e.vel.y = 0.0
