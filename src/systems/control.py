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
