import glm

from entity import EntityType
from tiles import TILE_SIZE


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
    if not state.center_cam_on_player:
        return
    player_entities = [e for e in state.active_entities if e.type == EntityType.PLAYER]
    if len(player_entities) == 0:
        return
    xs = [e.pos.x + e.size.x / 2 for e in player_entities]
    x = sum(xs, 0) / len(xs)
    x = int(x) + TILE_SIZE // 2
    y = TILE_SIZE * 4.5
    p = glm.vec2(x, y)
    graphics.camera.set_center(p)

    # if the stage is bigger than or equal to the cam size
    if state.stage.wc_dims.x >= graphics.camera.size.x:
        # make sure the cam pos doesnt go left of 0,0
        if graphics.camera.pos.x < 0:
            graphics.camera.pos.x = 0

        # make sure the cam right edge doesnt go past the stage right edge
        cam_right_edge = graphics.camera.pos.x + graphics.camera.size.x
        stage_right_edge = state.stage.wc_dims.x
        if cam_right_edge > stage_right_edge:
            graphics.camera.pos.x = stage_right_edge - graphics.camera.size.x


WALK_FORCE = 0.2
RUN_FORCE = 0.5
JUMP_FORCE = -3.6
RUNNING_JUMP_FORCE = -4.8


def control_entities(state):
    controllable_entities = [e for e in state.active_entities if e.input_controlled]
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
        if state.inputs.jump:
            if e.grounded or e.coyote_timer is not None and e.coyote_timer.can_jump():
                if state.inputs.run and abs(e.vel.x) > (RUNNER_MAX_SPEED - 0.5):
                    e.vel.y = RUNNING_JUMP_FORCE
                else:
                    e.vel.y = JUMP_FORCE
                e.grounded = False
                if e.coyote_timer is not None:
                    e.coyote_timer.timer = 0


no_move_force = 0.3
WALKER_MAX_SPEED = 2.0
RUNNER_MAX_SPEED = 3.0


def speed_limit_controlled_entities(state):
    controllable_entities = [e for e in state.active_entities if e.input_controlled]

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


def step_coyote_timers(state):
    for e in state.active_entities:
        if e.coyote_timer is None:
            continue

        if e.grounded:
            e.coyote_timer.reset()
        else:
            e.coyote_timer.step()
