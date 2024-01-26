import copy
import glm
from sprites.sprite import Sprite


class SeriallyStoredAnimatedSprite(Sprite):
    def __init__(
        self,
        texture,
        sample_position,
        size,
        offset,
        num_frames,
        looping,
    ):
        self.texture = texture
        self.sample_position = sample_position
        self.size = size
        self.offset = offset
        self.num_frames = num_frames
        self.looping = looping

    def is_animated(self) -> bool:
        return True

    def get_num_frames(self) -> int:
        return self.num_frames

    def is_looping(self) -> bool:
        return self.looping

    def get_frame_pos(self, frame_num) -> glm.vec2:
        assert (
            frame_num < self.num_frames
        ), f"Invalid frame_num: {frame_num}. Total frames: {self.get_num_frames()}"

        pos = copy.deepcopy(self.sample_position)
        pos.x += frame_num * self.size.x
        return pos

    def get_frame_size(self, frame_num) -> glm.vec2:
        return self.size

    def get_frame_offset(self, frame_num) -> glm.vec2:
        return self.offset

    def __repr__(self):
        return f"SeriallyStoredAnimatedSprite(texture={self.texture}, sample_position={self.sample_position}, size={self.size}, num_frames={self.num_frames}, looping={self.looping})"
