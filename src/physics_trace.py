import json
from enum import Enum
from pathlib import Path

from entity import EntityType, get_entity_bounds, get_entity_feet, intersects


TRACE_PATH = Path(__file__).resolve().parent.parent / "logs" / "physics_trace.jsonl"
TRACKED_TYPES = {EntityType.PLAYER, EntityType.GOOMBOR}


def reset_physics_trace_file():
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACE_PATH.write_text("", encoding="utf-8")


def _serialize(value):
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, (int, float, str, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize(v) for v in value]
    if hasattr(value, "x") and hasattr(value, "y"):
        data = {"x": float(value.x), "y": float(value.y)}
        if hasattr(value, "z"):
            data["z"] = float(value.z)
        if hasattr(value, "w"):
            data["w"] = float(value.w)
        return data
    return str(value)


def _entity_snapshot(state, entity):
    tl, br = get_entity_bounds(entity.pos, entity.size)
    feet_tl, feet_br = get_entity_feet(entity.pos, entity.size)
    overlaps = []

    for other in state.active_entities:
        if other is entity:
            continue
        otl, obr = get_entity_bounds(other.pos, other.size)
        if intersects(tl, br, otl, obr):
            overlaps.append(
                {
                    "type": other.type.name if other.type else None,
                    "index": state.entities.index(other),
                    "tl": _serialize(otl),
                    "br": _serialize(obr),
                }
            )

    return {
        "index": state.entities.index(entity),
        "type": entity.type.name if entity.type else None,
        "pos": _serialize(entity.pos),
        "size": _serialize(entity.size),
        "vel": _serialize(entity.vel),
        "acc": _serialize(entity.acc),
        "bounds": {"tl": _serialize(tl), "br": _serialize(br)},
        "feet_bounds": {"tl": _serialize(feet_tl), "br": _serialize(feet_br)},
        "grounded": entity.grounded,
        "facing": _serialize(entity.facing),
        "display_state": _serialize(entity.display_state),
        "has_tile_collisions": entity.has_tile_collisions,
        "has_entity_collisions": entity.has_entity_collisions,
        "no_gravity": entity.no_gravity,
        "input_controlled": _serialize(entity.input_controlled),
        "always_active": entity.always_active,
        "is_sticky_platform": entity.is_sticky_platform,
        "stun_timer": entity.stun_timer,
        "hp": entity.hp,
        "invincible": entity.invincible,
        "coyote_timer": entity.coyote_timer.timer if entity.coyote_timer else None,
        "ai": entity.ai.__class__.__name__ if entity.ai else None,
        "overlaps": overlaps,
    }


def log_physics_state(frame, phase, state, graphics):
    tracked = [e for e in state.active_entities if e.type in TRACKED_TYPES]
    tracked.sort(key=lambda e: (e.type.value, state.entities.index(e)))

    camera = graphics.camera
    payload = {
        "frame": frame,
        "phase": phase,
        "stage_dims": _serialize(state.stage.dims),
        "active_entities": len(state.active_entities),
        "tracked_entities": len(tracked),
        "camera": {
            "pos": _serialize(camera.pos),
            "size": _serialize(camera.size),
            "center": _serialize(camera.get_center()),
        },
        "entities": [_entity_snapshot(state, e) for e in tracked],
    }

    with TRACE_PATH.open("a", encoding="utf-8") as trace_file:
        trace_file.write(json.dumps(payload, separators=(",", ":")))
        trace_file.write("\n")
