from asyncio import StreamReader

from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.constants import MAX_PACKET_LENGTH


class PacketReader:
    """Packet reader."""

    def __init__(self, reader: StreamReader) -> None:
        self._reader = reader

    async def read_varint(self) -> int:
        data = bytearray()

        while True:
            byte = await self._reader.readexactly(1)
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
