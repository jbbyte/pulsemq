import asyncio
from typing import List, Optional, Dict
from .message import Message
from .consumer import Consumer


class MessageQueue:
    """Stores and handles the messages sent into a queue and handles the communication between consumers."""

    def __init__(
        self,
        name: str,
        max_unacked: int = 100,
        ack_timeout: int = 10,
        log_level: str = "INFO",
        delivery_method: str = "ROUNDROBIN",
    ):
        """
        A message queue that stores messages, tracks ACKs and manages delivery to each consumer.

        Args:
            name (str): The unique name of the queue.
            max_unacked (int): Maximum number of messages unacknowledged before backing a consumer off.
            ack_timeout(int): Timeout in seconds to wait for an ACK before resending or DLQ.
        """
        self.name = name
        self.queue: asyncio.Queue[Message] = asyncio.Queue()
        self.delivery_method = delivery_method.upper()
        if self.delivery_method not in ["ROUNDROBIN", "FANOUT"]:
            raise ValueError(
                f"Delivery method '{self.delivery_method}' is not of value ['ROUNDROBIN', 'FANOUT']"
            )

        # Consumer UUID -> Consumer
        self.consumers: Dict[str, Consumer] = {}
        # Consumer UUID -> Messages
        self.unacked_messages: Dict[str, List[Message]] = {}

        self.max_unacked = max_unacked
        self.ack_timeout = ack_timeout
        self.lock = asyncio.Lock()

        self.log_level = log_level
        self.debug = True if log_level == "DEBUG" else False
        self.running = True

    def stop(self):
        self.running = False

    async def publish(self, message: Message):
        """Add a message into the queue."""
        await self.queue.put(message)

    def ack(self, consumer_uuid: str, message_id: str):
        """Mark a message as acknowledged."""
        if consumer_uuid not in self.unacked_messages:
            if self.debug:
                raise KeyError(f"Unknown consumer UUID: {consumer_uuid}, unable to ACK")
            else:
                return

        original_len = len(self.unacked_messages[consumer_uuid])
        new_messages = [
            msg for msg in self.unacked_messages[consumer_uuid] if msg.id != message_id
        ]

        if len(new_messages) == original_len:
            if self.debug:
                raise ValueError(
                    f"Message ID '{message_id}' not found for consumer, unable to ACK."
                )
            else:
                return

        self.unacked_messages[consumer_uuid] = new_messages

        if not new_messages:
            del self.unacked_messages[consumer_uuid]

    def register_consumer(self, consumer: Consumer):
        """Register a new consumer to this queue."""
        if consumer.id in self.consumers:
            if self.debug:
                raise KeyError(
                    f"Unable to register already existing consumer UUID: {consumer.id}"
                )
            else:
                return

        self.consumers[consumer.id] = consumer

    def unregister_consumer(self, consumer_id: str):
        """Remove a consumer from this queue."""
        if consumer_id in self.consumers:
            del self.consumers[consumer_id]
        else:
            if self.debug:
                raise KeyError(
                    f"Unable to delete non-existing consumer UUID: {consumer_id}"
                )
            else:
                return

    def handle_deliveries(self):
        raise NotImplementedError(
            "Delivery loop has not been implemented for MessageQueue yet"
        )

    def handle_acks(self):
        raise NotImplementedError(
            "Ack loop for messages has not been implemented for MessageQueue yet"
        )

    def dump_to_disk(self):
        raise NotImplementedError(
            "Dump to disk loop has not been implemented for MessageQueue yet"
        )

    def load_from_disk(self):
        raise NotImplementedError(
            "Load from disk has not been implemented for MessageQueue yet"
        )
