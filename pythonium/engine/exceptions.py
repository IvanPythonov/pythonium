from typing import Any, override


class Error(Exception):
    """Base exception class for all pythonium errors."""

    message: str

    @override
    def __init__(self, **context_kwargs: Any) -> None:
        context = ", ".join(
            f"{key}={context_kwargs[key]!r}" for key in context_kwargs
        )
        super().__init__(f"{self.message} ({context})")


class PacketNotFoundError(Error):
    """Exception raised when a packet is not found."""

    message = "Failed to resolve packet."


class DecodeError(Error):
    """Exception raised when a decode error occurs."""

    message = "Failed to decode incoming packet payload."


class EncodeError(Error):
    """Exception raised when a encode error occurs."""

    message = "Failed to encode outgoing packet payload."


class WriterError(Error):
    """Exception raised when a writer error occurs."""

    message = "Failed to write data to client socket."


class VarIntDecodeError(DecodeError):
    """Exception raised when a varint decode error occurs."""

    message = "Malformed VarInt detected."


class PacketTooLargeError(DecodeError):
    """Exceptions raised when a packet too large error occurs."""

    message = "Packet size exceeds server limits."


class ActionError(DecodeError):
    """Exceptions raised when a action error occurs."""

    message = "Invalid action."


class KickError(PacketNotFoundError):
    """Exceptions raised when a kick error occurs."""

    message = (
        PacketNotFoundError.message.removesuffix(".") + ", kick is impossible."
    )
