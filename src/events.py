from enum import Enum
from audio import Audio, Music, PlaySong
from entity import EntityType
from graphics import Graphics

from state import State
from systems.control import WALK_FORCE, WALKER_MAX_SPEED


class Event:
    def __init__(self):
        pass


class Side(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


class LevelWon(Event):
    def __init__(self, next_level):
        self.next_level = next_level


class EntityTileCollision:
    def __init__(self, entity, tile, tile_coord, side, pos, vel):
        self.entity = entity
        self.tile = tile
        self.tile_coord = tile_coord
        self.side = side
        self.pos = pos
        self.vel = vel


class EntityCollision(Event):
    def __init__(self, entity_a, entity_b, side):
        self.entity_a = entity_a
        self.entity_b = entity_b
        self.side = side


def handle_events(state: State, graphics: Graphics, audio: Audio):
    for event in state.events:
        match event:
            case LevelWon():
                # play a level win sound
                audio.events.append(PlaySong(Music.WIN))
                for e in state.entities:
                    if e.type == EntityType.PLAYER:
                        e.input_controlled = False
                        e.has_collisions = False
                        e.no_gravity = True
                        e.vel.x = WALKER_MAX_SPEED
                        e.invincible = True
                        state.center_cam_on_player = False

                        # make them walk to the right
                        # when they get off screen, load next stage
            case _:
                pass
    state.events.clear()
