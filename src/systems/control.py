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
    centers = [e.pos + e.size / 2 for e in player_entities]
    avg_center = sum(centers, glm.vec2(0, 0)) / len(centers)

    graphics.camera.center(avg_center)


def control_entities(state):
    move_force = 0.01

    controllable_entities = [e for e in state.entities if e.input_controlled]
    for e in controllable_entities:
        if state.inputs.left:
            e.acc.x -= move_force
        if state.inputs.right:
            e.acc.x += move_force
