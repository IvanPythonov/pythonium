import asyncio
from asyncio import StreamReader
from collections.abc import AsyncGenerator

from pythonium.engine.client import ClientSession
from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.constants import MAX_PACKET_LENGTH
from pythonium.engine.enums import Direction
from pythonium.engine.exceptions import PacketTooLargeError, VarIntDecodeError
from pythonium.engine.packets import Packet, PacketStorage, deserialize


class PacketReader:
    """Packet reader."""

    def __init__(self, reader: StreamReader) -> None:
        self._reader = reader
        self._buffer = bytearray(65536)
        self._cursor = 0
        self._limit = 0

    async def _ensure_data(self, n: int) -> None:
        while self._limit - self._cursor < n:
            if self._limit == len(self._buffer):
                remaining = self._limit - self._cursor
                self._buffer[:remaining] = self._buffer[
                    self._cursor : self._limit
                ]
                self._cursor = 0
                self._limit = remaining

            chunk = await self._reader.read(65536)
            if not chunk:
                raise StopAsyncIteration

            chunk_len = len(chunk)
            self._buffer[self._limit : self._limit + chunk_len] = chunk
            self._limit += chunk_len

    async def read_exactly(self, n: int) -> bytes:
        await self._ensure_data(n)
        data = self._buffer[self._cursor : self._cursor + n]
        self._cursor += n
        return bytes(data)

    async def read_varint(self) -> int:
        value = 0
        shift = 0

        for _ in range(5):
            if self._cursor >= self._limit:
                await self._ensure_data(1)

            byte = self._buffer[self._cursor]
            self._cursor += 1

            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                return value

            shift += 7

        raise VarIntDecodeError(
            value=value, shift=shift, cursor=self._cursor, limit=self._limit
        )

    async def read_packet(self) -> bytes:
        length = await self.read_varint()

        if length > MAX_PACKET_LENGTH:
            raise PacketTooLargeError(
                length=length, max_packet_length=MAX_PACKET_LENGTH
            )

        return await self.read_exactly(length)

    async def read(
        self, client_session: ClientSession
    ) -> AsyncGenerator[Packet]:
        while True:
            try:
                packet_data = await self.read_packet()
            except (asyncio.IncompleteReadError, StopAsyncIteration):
                return

            packet_id, consumed = VarIntCodec().deserialize(packet_data)

            model = PacketStorage.get(
                packet_id=packet_id,
                state=client_session.state,
                direction=Direction.SERVERBOUND,
            )

            if packet_id != model.packet_id:
                msg = (
                    f"Packet ID mismatch (expected {model.packet_id}, "
                    f" got {packet_id})"
                )
                raise ValueError(msg)

            yield deserialize(model, packet_data[consumed:])
