from entity import Facing


def step_sprite_animators(state):
    for e in state.entities:
        if e.sprite_animator is not None:
            e.sprite_animator.step()


def set_facing(state):
    for entity in state.entities:
        if entity.vel.x > 0.1:
            entity.facing = Facing.RIGHT
        elif entity.vel.x < -0.1:
            entity.facing = Facing.LEFT
