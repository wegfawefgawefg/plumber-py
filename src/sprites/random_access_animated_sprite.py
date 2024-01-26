import glm
from sprites.sprite import Sprite


class RandomAccessAnimatedSprite(Sprite):
    def __init__(
        self,
        texture,
        sample_positions,
        size,
        offset,
        looping,
    ):
        self.texture = texture
        self.sample_positions = sample_positions
        self.size = size
        self.offset = offset
        self.looping = looping

    def is_animated(self) -> bool:
        return True

    def get_num_frames(self) -> int:
        return len(self.sample_positions)

    def is_looping(self) -> bool:
        return self.looping

    def get_frame_pos(self, frame_num) -> glm.vec2:
        assert (
            frame_num < self.get_num_frames()
        ), f"Invalid frame_num: {frame_num}. Total frames: {self.get_num_frames()}"

        return self.sample_positions[frame_num]

    def get_frame_size(self, frame_num) -> glm.vec2:
        return self.size

    def get_frame_offset(self, frame_num) -> glm.vec2:
        return self.offset

    def __repr__(self):
        return f"RandomAccessAnimatedSprite(texture={self.texture}, sample_positions={self.sample_positions}, size={self.size}, looping={self.looping})"
