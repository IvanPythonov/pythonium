import asyncio
from asyncio import StreamReader
from collections.abc import AsyncGenerator
from logging import getLogger

from pythonium.engine.client import ClientSession
from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.constants import MAX_PACKET_LENGTH
from pythonium.engine.enums import Direction
from pythonium.engine.exceptions import PacketTooLargeError, VarIntDecodeError
from pythonium.engine.packets import Packet, PacketStorage, deserialize

logger = getLogger(__name__)


class PacketReader:
    """High-performance packet reader using a sliding window buffer."""

    def __init__(self, reader: StreamReader) -> None:
        self._reader = reader
        self._buffer = bytearray()
        self._cursor = 0
        self._cleanup_threshold = 131072

    async def _fill_buffer(self) -> None:
        if self._cursor > self._cleanup_threshold:
            del self._buffer[: self._cursor]
            self._cursor = 0

        chunk = await self._reader.read(65536)
        if not chunk:
            raise asyncio.IncompleteReadError(
                bytes(self._buffer[self._cursor :]), None
            )

        self._buffer.extend(chunk)

    async def read_exactly(self, n: int) -> memoryview:
        while len(self._buffer) - self._cursor < n:
            await self._fill_buffer()

        start = self._cursor
        self._cursor += n

        return memoryview(self._buffer)[start : self._cursor]

    async def read_varint(self) -> int:
        value = 0
        shift = 0

        for _ in range(5):
            if self._cursor >= len(self._buffer):
                await self._fill_buffer()

            byte = self._buffer[self._cursor]
            self._cursor += 1

            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                return value

            shift += 7

        raise VarIntDecodeError(
            value=value,
            shift=shift,
            cursor=self._cursor,
            limit=len(self._buffer),
        )

    async def read_packet_data(self) -> bytes:
        length = await self.read_varint()

        if length > MAX_PACKET_LENGTH:
            raise PacketTooLargeError(
                length=length, max_packet_length=MAX_PACKET_LENGTH
            )

        packet_view = await self.read_exactly(length)
        return bytes(packet_view)

    async def read(
        self, client_session: ClientSession
    ) -> AsyncGenerator[Packet]:
        varint_codec = VarIntCodec()

        while True:
            try:
                packet_data = await asyncio.wait_for(
                    self.read_packet_data(), timeout=20.0
                )
            except TimeoutError:
                logger.warning("Client timed out (no packets for 20s).")
                return
            except (asyncio.IncompleteReadError, ConnectionError):
                return

            packet_id, consumed = varint_codec.deserialize(packet_data)

            model = PacketStorage.get(
                packet_id=packet_id,
                state=client_session.state,
                direction=Direction.SERVERBOUND,
            )

            yield deserialize(model, packet_data[consumed:])
