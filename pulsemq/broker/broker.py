import asyncio
from typing import Dict, Optional
from .queue import MessageQueue


class Broker:
    """Defines a broker that can attach to a TCP server to handle client connection commands."""

    def __init__(self, log_level: str = "INFO"):
        """
        A broker that orchestrates queues and abstracts client connection commands from the network modules.
        """
        # QueueName -> MQ Class
        self.queues: Dict[str, MessageQueue] = {}

        self.log_level = log_level.upper()
        self.debug = True if log_level == "DEBUG" else False

    def add_queue(self, queue: MessageQueue):
        """Add a queue to the broker."""
        if queue.name in self.queues:
            if self.debug:
                raise KeyError(
                    f"Unable to add queue to Broker since {queue.name} is already present."
                )
            else:
                return

        self.queues[queue.name] = queue

    def remove_queue(self, queue_name: str):
        """Remove a queue from the broker."""
        if queue_name not in self.queues:
            if self.debug:
                raise KeyError(
                    f"Unable to remove queue from Broker since {queue_name} is not present."
                )
            else:
                return

        self.queues[queue_name].stop()
        del self.queues[queue_name]

    def get_queue(self, queue_name: str) -> Optional[MessageQueue]:
        """Get a queue in a broker's queue list. Will return the MessageQueue or None if it does not exist."""
        return self.queues.get(queue_name)
