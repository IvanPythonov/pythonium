from pythonium.engine.enums.states import State


def get_next_state(id_: int) -> State:
    return State(id_ + 1)


NextState = get_next_state
