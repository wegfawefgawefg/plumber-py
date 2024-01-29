from pprint import pprint

from entity import EntityType, get_entity_bounds
from events import LevelWon
from state import Message, State
from tiles import TILE_SIZE


def exit_if_player_hits_exit_tile(state: State):
    if state.stage.won == True:
        return

    for e in state.active_entities:
        if e.type == EntityType.PLAYER:
            player_tile_pos = e.pos // TILE_SIZE
            player_tile_pos_tuple = (player_tile_pos.x, player_tile_pos.y)
            if player_tile_pos_tuple in state.stage.exits:
                state.stage.won = True
                exit = state.stage.exits[player_tile_pos_tuple]
                state.events.append(LevelWon(exit.goes_to))
                state.alerts.append(Message("Level complete!", 60))


def kill_entities_that_touch_the_bottom_void(state: State):
    pass
