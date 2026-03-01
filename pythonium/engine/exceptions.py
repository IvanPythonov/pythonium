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

    message = "Unknown packet."


class DecodeError(Error):
    """Exception raised when a decode error occurs."""

    message = "Decode error just occured."


class WriterError(Error):
    """Exception raised when a writer error occurs."""

    message = "Writer error just occured."


class VarIntDecodeError(DecodeError):
    """Exception raised when a varint decode error occurs."""

    message = "Tried to read too long of a VarInt"


class PacketTooLargeError(DecodeError):
    """Exceptions raised when a packet too large error occurs."""

    message = "Packet too large"
