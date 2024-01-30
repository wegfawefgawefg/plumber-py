def step_ai(state, graphics, audio):
    for e in state.active_entities:
        if e.ai:
            e.ai.step(e, state, graphics, audio)
