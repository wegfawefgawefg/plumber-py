import glm
from sprites.sprite import Sprite


class DynamicRandomAccessAnimatedSprite(Sprite):
    def __init__(self, texture, sample_positions, looping):
        self.texture = texture
        self.sample_positions = sample_positions
        self.looping = looping

    def is_animated(self) -> bool:
        return True

    def get_num_frames(self) -> int:
        return len(self.sample_positions)

    def is_looping(self) -> bool:
        return self.looping

    def get_frame_pos(self, frame_num: int) -> glm.vec2:
        assert (
            frame_num < self.get_num_frames()
        ), f"Invalid frame_num: {frame_num}. Total frames: {self.get_num_frames()}"

        return self.sample_positions[frame_num].pos

    def get_frame_size(self, frame_num: int) -> glm.vec2:
        assert (
            frame_num < self.get_num_frames()
        ), f"Invalid frame_num: {frame_num}. Total frames: {self.get_num_frames()}"

        return self.sample_positions[frame_num].size

    def get_frame_offset(self, frame_num: int) -> glm.vec2:
        return glm.vec2(0, 0)

    def __repr__(self) -> str:
        return f"DynamicRandomAccessAnimatedSprite(texture={self.texture}, sample_positions={self.sample_positions}, looping={self.looping})"
