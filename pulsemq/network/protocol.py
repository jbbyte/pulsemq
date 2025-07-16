import json
import asyncio

__DELIMITER = b"\n"


def __encode_message(data: dict) -> bytes:
    """Encode a dictionary into a protocol-safe byte stream."""
    return json.dumps(data).encode("utf-8") + __DELIMITER


def __decode_message(data: bytes) -> dict:
    """Decode a protocol message into a dictionary."""
    return json.loads(data.decode("utf-8").strip())


async def __read_message(reader: asyncio.StreamReader) -> dict:
    """Read a single complete message from the stream."""
    data = await reader.readuntil(__DELIMITER)
    return __decode_message(data)
