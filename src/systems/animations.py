def step_sprite_animators(state):
    for e in state.entities:
        if e.sprite_animator is not None:
            e.sprite_animator.step()
