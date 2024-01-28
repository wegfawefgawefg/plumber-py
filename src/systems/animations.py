from entity import DisplayState, Facing
from sprites.sprite_animator import DEFAULT_FRAME_DURATION


def step_sprite_animators(state):
    for e in state.entities:
        if e.sprite_animator is not None:
            e.sprite_animator.step()

    for d in state.stage.background_decorations:
        if d.sprite_animator is not None:
            d.sprite_animator.step()

    for d in state.stage.foreground_decorations:
        if d.sprite_animator is not None:
            d.sprite_animator.step()


FACING_THRESHOLD = 0.2


def set_facing(state):
    for entity in state.entities:
        if entity.vel.x > FACING_THRESHOLD:
            entity.facing = Facing.RIGHT
        elif entity.vel.x < -FACING_THRESHOLD:
            entity.facing = Facing.LEFT


WALKING_THRESHOLD = 1.5
RUNNING_THRESHOLD = 2.5


def update_display_states(state):
    for entity in state.entities:
        new_display_state = None
        new_animation_duration = None
        if entity.hp == 0:
            new_display_state = DisplayState.DEAD
            new_animation_duration = DEFAULT_FRAME_DURATION
        elif entity.stun_timer > 0:
            new_display_state = DisplayState.STUNNED
        elif abs(entity.vel.x) > RUNNING_THRESHOLD:
            new_animation_duration = DEFAULT_FRAME_DURATION / 2
        elif abs(entity.vel.x) > WALKING_THRESHOLD:
            new_display_state = DisplayState.WALKING
            new_animation_duration = DEFAULT_FRAME_DURATION
        else:
            new_display_state = DisplayState.NEUTRAL
            new_animation_duration = DEFAULT_FRAME_DURATION * 2

        if new_display_state != None and new_display_state != entity.display_state:
            entity.display_state = new_display_state
            entity.sprite_animator.update_sprite_based_on_display_state(
                entity.display_state
            )
            entity.sprite_animator.set_frame_duration(DEFAULT_FRAME_DURATION)

        if new_animation_duration != None:
            entity.sprite_animator.set_frame_duration(new_animation_duration)
