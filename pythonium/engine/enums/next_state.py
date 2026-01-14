from enum import IntEnum, auto, unique


@unique
class NextState(IntEnum):
    """
    Enum class representing next states of a client.

    Intents 2 and 3 both transition to the Login state, but 3 indicates
    that the client is connecting due to a Transfer packet received from
    another server. If the server is not expecting transfers, it may choose
    to reject the connection by replying with a Disconnect (login) packet.
    """

    STATUS = auto()
    LOGIN = auto()
    TRANSFER = auto()
