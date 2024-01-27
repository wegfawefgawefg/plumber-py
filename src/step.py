import pygame
from entity import EntityType
from render import mouse_pos

from state import Mode
import systems
from systems.animations import set_facing, step_sprite_animators
from systems.control import (
    center_cam_on_player,
    control_camera,
    control_entities,
    speed_limit_controlled_entities,
    step_coyote_timers,
)
from systems.physics import (
    gravity,
    physics_post_step,
    set_grounded,
    zero_accelerations,
)


def step_playing(state, graphics):
    # control_camera(state, graphics)
    step_sprite_animators(state)
    set_facing(state)
    zero_accelerations(state)
    gravity(state)
    set_grounded(state)
    step_coyote_timers(state)

    control_entities(state)
    speed_limit_controlled_entities(state)
    physics_post_step(state)

    center_cam_on_player(state, graphics)

    state.events.clear()

    some_debug_messages(state, graphics)


def some_debug_messages(state, graphics):
    # print player position
    player_entities = [e for e in state.entities if e.type == EntityType.PLAYER]
    if len(player_entities) > 0:
        player = player_entities[0]
        state.debug_messages.append(f"player pos: {player.pos}")

    # print cam position
    state.debug_messages.append(f"cam pos: {graphics.camera.pos}")
    # print cam center
    state.debug_messages.append(f"cam center: {graphics.camera.get_center()}")

    # player facing
    state.debug_messages.append(f"player facing: {player.facing}")

    # player vel
    state.debug_messages.append(f"player vel: {player.vel}")

    # print coyote timer
    if len(player_entities) > 0:
        player = player_entities[0]
        state.debug_messages.append(f"coyote timer: {player.coyote_timer.timer}")

    # print player grounded
    state.debug_messages.append(f"player grounded: {player.grounded}")

    # print mouse pos
    state.debug_messages.append(f"mouse pos: {mouse_pos(graphics)}")


def step_pause(state, graphics):
    pass


def step(state, graphics):
    match state.mode:
        case Mode.PLAYING:
            step_playing(state, graphics)
        case Mode.PAUSE:
            step_pause(state, graphics)
