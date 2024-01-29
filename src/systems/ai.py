def step_ai(state):
    for e in state.active_entities:
        if e.ai:
            e.ai.step(e)
