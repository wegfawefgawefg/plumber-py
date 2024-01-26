import glm


class Sprite:
    def is_animated(self) -> bool:
        raise NotImplementedError

    def get_num_frames(self) -> int:
        raise NotImplementedError

    def is_looping(self) -> bool:
        raise NotImplementedError

    def get_frame_pos(self, frame_num: int) -> glm.vec2:
        raise NotImplementedError

    def get_frame_size(self, frame_num: int) -> glm.vec2:
        raise NotImplementedError

    def get_frame_offset(self, frame_num: int) -> glm.vec2:
        raise NotImplementedError
