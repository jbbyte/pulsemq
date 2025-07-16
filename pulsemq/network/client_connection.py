import asyncio
from typing import TYPE_CHECKING, Optional
from .protocol import __read_message, __encode_message

if TYPE_CHECKING:
    from pulsemq.broker.broker import Broker


class ClientConnection:
    """Defines a client connection which is created from a TCP server."""

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        broker: Broker,
        log_level: str = "INFO",
    ):
        self.reader = reader
        self.writer = writer
        self.broker = broker

        self.peername = writer.get_extra_info("peername")
        self.consumer_id: Optional[str] = None
        self.running = True

        self.log_level = log_level
        self.debug = True if log_level == "DEBUG" else False

    async def handle(self):
        """Main loop for handling client connection."""
        try:
            while self.running:
                msg = await __read_message(self.reader)
                await self.handle_message(msg)
        except asyncio.IncompleteReadError:
            if self.debug:
                print(
                    f"[DEBUG ERROR] Caught an incomplete read error while in main handle loop for {self.peername}"
                )
            pass
        except Exception as e:
            print(
                f"[ERROR] Caught a non-incomplete read error from {self.peername} in main handle loop. Error was {e}"
            )
        finally:
            self.writer.close()
            await self.writer.wait_closed()

    async def handle_message(self, message: dict):
        """Process a message from the client."""
        raise NotImplementedError("Not implemented ClientConnection.handle_message")
