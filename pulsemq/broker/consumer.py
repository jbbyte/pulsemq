from typing import Optional
import uuid
import time


class Consumer:
    """A consumer will be able to ingest data that is inserted into message queues."""

    def __init__(self, connection, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.connection = connection
        self.last_ping = time.time()
        self.error_count = 0

    def request_shutdown(self):
        """Request the consumer to shutdown and not reconnect."""
        return NotImplementedError(
            "Request shutdown has not been implemented for Consumer yet"
        )

    def request_reconnect_after_delay(self, delay: int = 30):
        """Request the consumer to reconnect after {delay} seconds."""
        return NotImplementedError(
            "Request reconnect after delay has not been implemented for Consumer yet"
        )
