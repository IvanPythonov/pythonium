from typing import Any, override


class Error(Exception):
    """Base exception class for all pythonium errors."""

    message: str = "Unknown error"
    show_in_production: bool = False

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


class VarIntEncodeError(EncodeError):
    """Exception raised when a varint encode error occurs."""

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


class PacketNotHandledError(PacketNotFoundError):
    """Exception raised when a packet is not handled."""

    message = (
        PacketNotFoundError.message.removesuffix(".") + ", no handler found."
    )


class ChunkSectionOutOfBoundsError(Error):
    """Exception raised when a chunk section is out of bounds."""

    message = "Chunk section Y coordinate is out of bounds."


class SuspiciousClientError(Error):
    """Exception raised when a suspicious client is detected."""

    message = "Client has no UUID or username after configuration phase."

    show_in_production = True


class IncorrectIdentifierError(Error):
    """Exception raised when a identifier is incorrect."""

    message = "Invalid identifier."
