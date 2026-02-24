from dataclasses import dataclass


SIDE_LEFT = "left"
SIDE_RIGHT = "right"
SIDE_UP = "up"
SIDE_DOWN = "down"


@dataclass(frozen=True)
class TileContactEvent:
    entity_index: int
    entity_type: str | None
    tile_coord: tuple[int, int]
    side: str


@dataclass(frozen=True)
class EntityContactEvent:
    entity_a_index: int
    entity_a_type: str | None
    entity_b_index: int
    entity_b_type: str | None
    side_a: str
    side_b: str
    axis: str


def reset_entity_contact_summaries(state):
    for entity in state.active_entities:
        entity.blocked_left = False
        entity.blocked_right = False
        entity.blocked_up = False
        entity.blocked_down = False
        entity.touching_entities.clear()
        entity.touching_tiles.clear()


def _entity_index(state, entity):
    return state.entities.index(entity)


def _emit_physics_event(state, key, event):
    if key in state._physics_event_keys:
        return
    state._physics_event_keys.add(key)
    state.physics_events.append(event)


def mark_blocked_for_delta(entity, axis, delta):
    if axis == "x":
        if delta > 0:
            entity.blocked_right = True
        elif delta < 0:
            entity.blocked_left = True
    else:
        if delta > 0:
            entity.blocked_down = True
        elif delta < 0:
            entity.blocked_up = True


def register_tile_contacts(state, entity, axis, delta, collided_pairs):
    if not collided_pairs:
        return

    if axis == "x":
        side = SIDE_RIGHT if delta > 0 else SIDE_LEFT
    else:
        side = SIDE_DOWN if delta > 0 else SIDE_UP

    entity_index = _entity_index(state, entity)
    entity_type = entity.type.name if entity.type else None

    for pair in collided_pairs:
        coord = (int(pair.coord.x), int(pair.coord.y))
        touch_record = (coord, side)
        if touch_record not in entity.touching_tiles:
            entity.touching_tiles.append(touch_record)

        key = ("tile_contact", entity_index, coord, side)
        _emit_physics_event(
            state,
            key,
            TileContactEvent(
                entity_index=entity_index,
                entity_type=entity_type,
                tile_coord=coord,
                side=side,
            ),
        )


def _side_from_separation_direction(axis, separation_dir):
    # separation_dir is where the entity was moved to separate.
    # The contact side is opposite of that movement.
    if axis == "x":
        return SIDE_RIGHT if separation_dir < 0 else SIDE_LEFT
    return SIDE_DOWN if separation_dir < 0 else SIDE_UP


def register_entity_contact(state, entity_a, entity_b, axis, a_dir, b_dir):
    side_a = _side_from_separation_direction(axis, a_dir)
    side_b = _side_from_separation_direction(axis, b_dir)

    if side_a == SIDE_LEFT:
        entity_a.blocked_left = True
    elif side_a == SIDE_RIGHT:
        entity_a.blocked_right = True
    elif side_a == SIDE_UP:
        entity_a.blocked_up = True
    else:
        entity_a.blocked_down = True

    if side_b == SIDE_LEFT:
        entity_b.blocked_left = True
    elif side_b == SIDE_RIGHT:
        entity_b.blocked_right = True
    elif side_b == SIDE_UP:
        entity_b.blocked_up = True
    else:
        entity_b.blocked_down = True

    a_index = _entity_index(state, entity_a)
    b_index = _entity_index(state, entity_b)
    a_type = entity_a.type.name if entity_a.type else None
    b_type = entity_b.type.name if entity_b.type else None

    a_touch = (b_index, b_type, side_a)
    if a_touch not in entity_a.touching_entities:
        entity_a.touching_entities.append(a_touch)

    b_touch = (a_index, a_type, side_b)
    if b_touch not in entity_b.touching_entities:
        entity_b.touching_entities.append(b_touch)

    lo = min(a_index, b_index)
    hi = max(a_index, b_index)
    key = ("entity_contact", lo, hi, axis, side_a, side_b)
    _emit_physics_event(
        state,
        key,
        EntityContactEvent(
            entity_a_index=a_index,
            entity_a_type=a_type,
            entity_b_index=b_index,
            entity_b_type=b_type,
            side_a=side_a,
            side_b=side_b,
            axis=axis,
        ),
    )
