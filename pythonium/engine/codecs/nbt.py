import io

from nbtlib import Compound
from nbtlib.nbt import File

from pythonium.engine.codecs.base import Codec
from pythonium.engine.typealiases import Deserialized


class NBTCodec(Codec[Compound]):
    """
    NBT type implementation with Minecraft protocol serialization.

    The NBT format is currently used in several places, chiefly:

    In the Protocol as part of Slot Data
    Multiplayer saved server list (servers.dat).
    Player data (both single player and multiplayer, one file per player).
    Saved worlds (both single player and multiplayer).
        World index file (level.dat) that contains general information
        Chunk data (see Region Files)
    """

    def serialize(self, *, field: Compound) -> bytes:
        buffer = io.BytesIO()
        file = File(field, gzipped=False)
        file.write(buffer)

        data = buffer.getvalue()

        prefix = b"\x0a\x00\x00"
        if data.startswith(prefix):
            payload = data.removeprefix(prefix)
            return b"\x0a" + payload

        return data

    def deserialize(self, data: bytes) -> Deserialized[Compound]:
        buffer = io.BytesIO(data)

        value = Compound.parse(buffer)

        return value, buffer.tell()
