import glm

from entity import EntityType


def control_camera(state, graphics):
    cam_speed = 1

    if state.inputs.camera_left:
        graphics.camera.pos.x -= cam_speed
    if state.inputs.camera_right:
        graphics.camera.pos.x += cam_speed
    if state.inputs.camera_up:
        graphics.camera.pos.y -= cam_speed
    if state.inputs.camera_down:
        graphics.camera.pos.y += cam_speed


def center_cam_on_player(state, graphics):
    player_entities = [e for e in state.entities if e.type == EntityType.PLAYER]
    if len(player_entities) == 0:
        return
    centers = [(e.pos + e.size / 2.0) for e in player_entities]
    avg_center = glm.vec2(0, 0)
    for c in centers:
        avg_center += c
    avg_center /= float(len(centers))
    # avg_center = glm.vec2(0, 0)
    state.debug_messages.append(f"avg_center: {avg_center}")

    graphics.camera.set_center(avg_center)


WALK_FORCE = 0.2
RUN_FORCE = 0.5


def control_entities(state):
    controllable_entities = [e for e in state.entities if e.input_controlled]
    for e in controllable_entities:
        if state.inputs.left:
            if state.inputs.run:
                e.acc.x -= RUN_FORCE
            else:
                e.acc.x -= WALK_FORCE
        if state.inputs.right:
            if state.inputs.run:
                e.acc.x += RUN_FORCE
            else:
                e.acc.x += WALK_FORCE

        # if state.inputs.up:
        #     e.acc.y -= move_force
        # if state.inputs.down:
        #     e.acc.y += move_force
        if state.inputs.jump and e.grounded:
            e.vel.y = -4.5
            e.grounded = False


no_move_force = 0.2
WALKER_MAX_SPEED = 2.0
RUNNER_MAX_SPEED = 3.0


def speed_limit_controlled_entities(state):
    controllable_entities = [e for e in state.entities if e.input_controlled]

    for e in controllable_entities:
        if e.input_controlled:
            if state.inputs.right:
                if state.inputs.run:
                    e.vel.x = min(e.vel.x, RUNNER_MAX_SPEED)
                else:
                    e.vel.x = min(e.vel.x, WALKER_MAX_SPEED)
            else:
                # slow down
                if e.vel.x > 0:
                    e.acc.x = max(-no_move_force, -e.vel.x)
                pass

            if state.inputs.left:
                if state.inputs.run:
                    e.vel.x = max(e.vel.x, -RUNNER_MAX_SPEED)
                else:
                    e.vel.x = max(e.vel.x, -WALKER_MAX_SPEED)
            else:
                # slow down
                if e.vel.x < 0:
                    e.acc.x = max(no_move_force, e.vel.x)
