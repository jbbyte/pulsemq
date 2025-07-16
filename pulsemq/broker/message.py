import uuid
import time
from typing import Optional, Dict


class Message:
    """The contents and ACK related information of a message sent into a message queue."""

    def __init__(self, data: str, msg_id: Optional[str] = None):
        self.id = msg_id or str(uuid.uuid4())
        self.data = data
        self.timestamp = time.time()

        # Consumer ID -> Last time as float (time.time())
        self.last_acks: Dict[str, float] = {}
