from enum import Enum
import time
from small_ass_cache import AssetCache, loader

import pygame


def load_sound(path):
    return pygame.mixer.Sound(path)


def load_song(path):
    return path
    # return pygame.mixer.music.load(path)


class Audio:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.sounds = AssetCache()
        self.music = AssetCache()


@loader(load_sound, path="assets/sounds/")
class Sounds(Enum):
    JUMP = "jump.ogg"


@loader(load_song, path="assets/music/")
class Music(Enum):
    SHITTING = "shitting.ogg"


if __name__ == "__main__":
    audio = Audio()
    # while True:
    #     jump_sound = audio.sounds.get(Sounds.JUMP)
    #     jump_sound.set_volume(0.1)
    #     jump_sound.play()
    #     time.sleep(1)

    music_path = audio.sounds.get(Music.SHITTING)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    # lower volume
    # pygame.mixer.music.fadeout(5000)

    while True:
        pass
