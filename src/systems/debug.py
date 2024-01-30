from sre_parse import State

from state import Message


def debug_collisions(state: State):
    # state.alerts.append(Message("Test Collision Alert", 2))
    # state.debug_messages.append("Test Debug Message")
    for event in state.events:
        state.debug_messages.append(str(event))
    for e in state.active_entities:
        # entity positions
        state.debug_messages.append(f"{e.type} pos: {e.pos}")
