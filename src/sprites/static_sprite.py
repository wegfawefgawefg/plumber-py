import glm

from sprites.sprite import Sprite


class StaticSprite(Sprite):
    def __init__(self, texture, sample_position: glm.vec2, size: glm.vec2) -> None:
        self.texture = texture
        self.sample_position = sample_position
        self.size = size
        self.offset = glm.vec2(0, 0)

    def is_animated(self) -> bool:
        return False

    def get_num_frames(self) -> int:
        return 1

    def is_looping(self) -> bool:
        return False

    def get_frame_pos(self, frame_num: int) -> glm.vec2:
        return self.sample_position

    def get_frame_size(self, frame_num: int) -> glm.vec2:
        return self.size

    def get_frame_offset(self, frame_num: int) -> glm.vec2:
        return self.offset

    def __repr__(self) -> str:
        return f"StaticSprite(texture={self.texture}, sample_position={self.sample_position}, size={self.size})"
