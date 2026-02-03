from __future__ import annotations

import gzip
import logging
import zlib
from binascii import hexlify
from io import BytesIO

from pynbt import (
    NBTFile,
    TAG_Byte,
    TAG_Byte_Array,
    TAG_Compound,
    TAG_Double,
    TAG_Float,
    TAG_Int,
    TAG_Int_Array,
    TAG_List,
    TAG_Long,
    TAG_Long_Array,
    TAG_Short,
    TAG_String,
)

from pythonium.engine.codecs.base import Codec
from pythonium.engine.typealiases import Deserialized

LOGGER = logging.getLogger(__name__)

# Common magic bytes
TAG_COMPOUND = 0x0A
GZIP_MAGIC_FIRST = 0x1F
GZIP_MAGIC_SECOND = 0x8B

ZLIB_MAGIC = 0x78

# Numeric limits for NBT numeric tag selection
BYTE_MIN = -128
BYTE_MAX = 127
SHORT_MIN = -32768
SHORT_MAX = 32767
INT_MIN = -2147483648
INT_MAX = 2147483647
GZIP_HEADER_LEN = 2


def _ensure_tag(value: object) -> object:  # noqa: C901, PLR0911, PLR0912
    """
    Convert a Python value into a PyNBT TAG_* instance.

    The function accepts already-constructed tag objects (objects that
    expose a ``write`` method) and common Python primitives (dict, list,
    str, int, float, bytes). It returns the corresponding PyNBT tag.
    """
    # If already a tag-like object, pass through
    if hasattr(value, "write"):
        return value

    # Compound/dict
    if isinstance(value, dict):
        comp = TAG_Compound({})
        for k, v in value.items():
            comp[k] = _ensure_tag(v)
        return comp

    # Byte array
    if isinstance(value, (bytes, bytearray)):
        return TAG_Byte_Array(bytes(value))

    # List -> TAG_List with inferred inner type
    if isinstance(value, list):
        if not value:
            return TAG_List(TAG_Compound, [])
        first = _ensure_tag(value[0])
        inner_cls = type(first)
        items = [(_ensure_tag(v)) for v in value]
        return TAG_List(inner_cls, items)

    # Strings
    if isinstance(value, str):
        return TAG_String(value)

    # Booleans -> store as byte
    if isinstance(value, bool):
        return TAG_Byte(1 if value else 0)

    # Numbers
    if isinstance(value, int):
        if BYTE_MIN <= value <= BYTE_MAX:
            return TAG_Byte(value)
        if SHORT_MIN <= value <= SHORT_MAX:
            return TAG_Short(value)
        if INT_MIN <= value <= INT_MAX:
            return TAG_Int(value)
        return TAG_Long(value)

    if isinstance(value, float):
        return TAG_Double(value)

    # Fallback: serialize as string
    return TAG_String(str(value))


class NBTCodec(Codec[dict]):
    """
    Codec for NBT values using PyNBT.

    Serializes a TAG_Compound (or Python `dict` convertible to one) into
    the on-wire NBT representation and parses it back.
    """

    __serializable_type__ = dict

    def serialize(self, *, field: dict) -> bytes:
        if field is None:
            tag = TAG_Compound({})
        elif hasattr(field, "write"):
            tag = field
        else:
            tag = _ensure_tag(field)

        bio = BytesIO()
        nbt = NBTFile(value=tag)
        nbt.save(bio)
        return bio.getvalue()

    def deserialize(self, data: bytes) -> Deserialized[dict]:
        if not data:
            return {}, 0

        start_pos = _find_nbt_start(data)
        nbt, consumed = _parse_nbt_with_recovery(data, start_pos)
        return _from_tag(nbt), consumed


class _TagCodec(Codec[object]):
    """Codec for a single NBT tag stored under the key 'value'."""

    def __init__(self, tag_cls: type[object]) -> None:
        self.tag_cls = tag_cls

    def serialize(self, *, field: object) -> bytes:
        tag = field if hasattr(field, "write") else _ensure_tag(field)
        compound = TAG_Compound({})
        compound["value"] = tag
        bio = BytesIO()
        NBTFile(value=compound).save(bio)
        return bio.getvalue()

    def deserialize(self, data: bytes) -> Deserialized[object]:
        nbt_codec = NBTCodec()
        obj, consumed = nbt_codec.deserialize(data)
        if not isinstance(obj, dict) or "value" not in obj:
            msg = "Expected compound with key 'value' for tag codec"
            raise ValueError(msg)
        return obj["value"], consumed


# Convenience constructors
def nbt_byte_codec() -> _TagCodec:
    return _TagCodec(TAG_Byte)


def nbt_short_codec() -> _TagCodec:
    return _TagCodec(TAG_Short)


def nbt_int_codec() -> _TagCodec:
    return _TagCodec(TAG_Int)


def nbt_long_codec() -> _TagCodec:
    return _TagCodec(TAG_Long)


def nbt_float_codec() -> _TagCodec:
    return _TagCodec(TAG_Float)


def nbt_double_codec() -> _TagCodec:
    return _TagCodec(TAG_Double)


def nbt_byte_array_codec() -> _TagCodec:
    return _TagCodec(TAG_Byte_Array)


def nbt_string_codec() -> _TagCodec:
    return _TagCodec(TAG_String)


def nbt_list_codec() -> _TagCodec:
    return _TagCodec(TAG_List)


def nbt_compound_codec() -> _TagCodec:
    return _TagCodec(TAG_Compound)


def nbt_int_array_codec() -> _TagCodec:
    return _TagCodec(TAG_Int_Array)


def nbt_long_array_codec() -> _TagCodec:
    return _TagCodec(TAG_Long_Array)


# Backwards-compatible uppercase aliases (kept for external callers)
NBT_Byte_Codec = nbt_byte_codec
NBT_Short_Codec = nbt_short_codec
NBT_Int_Codec = nbt_int_codec
NBT_Long_Codec = nbt_long_codec
NBT_Float_Codec = nbt_float_codec
NBT_Double_Codec = nbt_double_codec
NBT_Byte_Array_Codec = nbt_byte_array_codec
NBT_String_Codec = nbt_string_codec
NBT_List_Codec = nbt_list_codec
NBT_Compound_Codec = nbt_compound_codec
NBT_Int_Array_Codec = nbt_int_array_codec
NBT_Long_Array_Codec = nbt_long_array_codec


def _decode_varint(buf: bytes) -> tuple[int, int]:
    value = 0
    for i in range(min(5, len(buf))):
        b = buf[i]
        value |= (b & 0x7F) << (7 * i)
        if not (b & 0x80):
            return value, i + 1
    msg = "VarInt too long or incomplete"
    raise ValueError(msg)


def _find_nbt_start(data: bytes) -> int:
    try:
        _, c1 = _decode_varint(data)
        try:
            _, c2 = _decode_varint(data[c1:])
            cand = c1 + c2
            if cand < len(data) and data[cand] == TAG_COMPOUND:
                return cand
            if c1 < len(data) and data[c1] == TAG_COMPOUND:
                return c1
            msg = "no TAG_Compound at decoded varint positions"
            raise ValueError(msg)  # noqa: TRY301
        except ValueError:
            if c1 < len(data) and data[c1] == TAG_COMPOUND:
                return c1
            raise
    except Exception:  # noqa: BLE001 - varint decode may raise various errors
        limit = min(len(data), 64)
        for i in range(limit):
            if data[i] == TAG_COMPOUND:
                return i
        msg = "NBT data does not contain TAG_Compound in first bytes"
        raise ValueError(msg)  # noqa: B904


def _parse_nbt_with_recovery(
    data: bytes, start_pos: int
) -> tuple[object, int]:
    bio = BytesIO(data[start_pos:])
    try:
        nbt = NBTFile(io=bio)
        return nbt, start_pos + bio.tell()
    except Exception as exc:
        emsg = str(exc).lower()
        if "unsupported tag" in emsg or "unsupported tag type" in emsg:
            sample = data[start_pos : start_pos + 128]
            sample_hex = hexlify(sample).decode("ascii")
            first_bytes = data[:32]
            first_hex = hexlify(first_bytes).decode("ascii")
            msg = (
                f"PyNBT error: {exc!r}; likely caused by unexpected bytes at"
                "stream start."
                f" start_pos={start_pos}; sample(hex)={sample_hex};"
                f"first_bytes(hex)={first_hex}"
            )
            raise ValueError(msg) from exc

    sample = data[start_pos : start_pos + 512]
    sample_hex = hexlify(sample).decode("ascii")

    # Scan for later TAG_Compound candidates
    for i in range(start_pos, len(data)):
        if data[i] != TAG_COMPOUND:
            continue
        try:
            bio2 = BytesIO(data[i:])
            nbt = NBTFile(io=bio2)
            return nbt, i + bio2.tell()
        except Exception as exc:  # noqa: BLE001 - parsing error, try next
            LOGGER.debug("NBT parse attempt at offset %s failed: %s", i, exc)

    # Try gzip
    if (
        len(sample) >= 2  # noqa: PLR2004
        and sample[0] == GZIP_MAGIC_FIRST
        and sample[1] == GZIP_MAGIC_SECOND
    ):
        try:
            dec = gzip.decompress(data[start_pos:])
            nbt = NBTFile(io=BytesIO(dec))
            return nbt, start_pos + len(data[start_pos:])
        except Exception as exc2:
            msg = f"PyNBT failed to read gzip-compressed NBT: {exc2!r};"
            "sample(hex)={sample_hex}"
            raise ValueError(msg) from exc2

    # Try zlib
    if len(sample) >= 1 and sample[0] == ZLIB_MAGIC:
        try:
            dec = zlib.decompress(data[start_pos:])
            nbt = NBTFile(io=BytesIO(dec))
            return nbt, start_pos + len(data[start_pos:])
        except Exception as exc2:
            msg = (
                f"PyNBT failed to read zlib-compressed NBT: {exc2!r};"
                f"sample(hex)={sample_hex}"
            )
            raise ValueError(msg) from exc2

    first_bytes = data[:32]
    first_hex = hexlify(first_bytes).decode("ascii")
    msg = (
        f"PyNBT parse error: ; start_pos={start_pos};"
        f"sample(hex)={sample_hex}; first_bytes(hex)={first_hex}"
    )
    raise ValueError(msg)


def _from_tag(tag: object) -> object:  # noqa: PLR0911
    # Compound -> dict
    if isinstance(tag, TAG_Compound):
        out: dict[str, object] = {}
        for k, v in tag.items():
            out[k] = _from_tag(v)
        return out

    if isinstance(tag, TAG_List):
        # TAG_List may expose .value or be iterable
        try:
            seq = tag.value
        except Exception as exc:  # noqa: BLE001
            LOGGER.debug("TAG_List.value access failed: %s", exc)
            seq = list(tag)
        return [_from_tag(x) for x in seq]

    if isinstance(tag, TAG_String):
        return tag.value

    if isinstance(
        tag, (TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double)
    ):
        if isinstance(tag, (TAG_Float, TAG_Double)):
            return float(tag.value)
        return int(tag.value)

    if isinstance(tag, (TAG_Byte_Array, TAG_Int_Array, TAG_Long_Array)):
        return list(tag.value)

    # Fallback: try .value attribute
    try:
        return tag.value
    except Exception as exc:  # noqa: BLE001
        LOGGER.debug("Returning raw tag due to: %s", exc)
        return tag


__all__ = (
    "NBTCodec",
    "NBT_Byte_Array_Codec",
    "NBT_Byte_Codec",
    "NBT_Compound_Codec",
    "NBT_Double_Codec",
    "NBT_Float_Codec",
    "NBT_Int_Array_Codec",
    "NBT_Int_Codec",
    "NBT_List_Codec",
    "NBT_Long_Array_Codec",
    "NBT_Long_Codec",
    "NBT_Short_Codec",
    "NBT_String_Codec",
    "TAG_Byte",
    "TAG_Byte_Array",
    "TAG_Compound",
    "TAG_Double",
    "TAG_Float",
    "TAG_Int",
    "TAG_Int_Array",
    "TAG_List",
    "TAG_Long",
    "TAG_Long_Array",
    "TAG_Short",
    "TAG_String",
)
