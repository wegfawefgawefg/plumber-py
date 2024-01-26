import glm


def physics_pre_step(state):
    for e in state.entities:
        e.acc = glm.vec2(0, 0)


def physics_step(state):
    for e in state.entities:
        e.vel += e.acc


def physics_post_step(state):
    for e in state.entities:
        e.pos += e.vel
