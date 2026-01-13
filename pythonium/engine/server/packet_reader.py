import asyncio
from asyncio import StreamReader
from collections.abc import AsyncGenerator

from pythonium.engine.client import ClientSession
from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.constants import MAX_PACKET_LENGTH
from pythonium.engine.enums import Direction
from pythonium.engine.packets import Packet, deserialize, get_model_by_id


class PacketReader:
    """Packet reader."""

    def __init__(self, reader: StreamReader) -> None:
        self._reader = reader

    async def read_varint(self) -> int:
        data = bytearray()

        while True:
            try:
                byte = await self._reader.readexactly(1)
            except asyncio.IncompleteReadError as error:
                raise StopAsyncIteration from error
            data.append(byte[0])

            value, consumed = VarIntCodec().deserialize(data)
            if consumed == len(data):
                return value

    async def read_packet(self) -> bytes:
        length = await self.read_varint()

        if length > MAX_PACKET_LENGTH:
            msg = "Packet too large"
            raise ValueError(msg)

        return await self._reader.readexactly(length)

    async def read(
        self, client_session: ClientSession
    ) -> AsyncGenerator[Packet]:
        while True:
            try:
                packet_data = await self.read_packet()
            except (asyncio.IncompleteReadError, StopAsyncIteration):
                return

            print(packet_data)

            packet_id, consumed = VarIntCodec().deserialize(packet_data)

            model = get_model_by_id(
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
