from enum import Enum


class Event:
    def __init__(self):
        pass


class Side(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


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
