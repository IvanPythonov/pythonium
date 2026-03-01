from asyncio import StreamReader, StreamWriter, wait_for
from typing import final

from pythonium.engine.constants import MAX_PACKET_LENGTH
from pythonium.engine.exceptions import WriterError


@final
class ClientConnection:
    """Class representing Minecraft client connection."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

        self.address: str = self.writer.get_extra_info("peername")[0]

    async def write(self, data: bytes) -> None:
        if self.writer.is_closing():
            raise WriterError(
                is_closed=self.writer.is_closing(),
                info="Transport is already closed.",
            )

        try:
            self.writer.write(data)
            await wait_for(self.writer.drain(), timeout=15.0)
        except (ConnectionResetError, BrokenPipeError, RuntimeError) as e:
            raise WriterError(error=e.__class__.__name__) from e

    async def read(self, n: int | None = None) -> bytes | None:
        return await self.reader.read(n or MAX_PACKET_LENGTH)

    async def disconnect(self) -> None:
        """Disconnect the client from the server."""
        self.writer.close()
        await self.writer.wait_closed()
