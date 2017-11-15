from procsim.back_end.broadcast_bus import BroadcastBus

class BusLog(BroadcastBus):
    """BusLog logs all the values published to it.

    Attributes:
        log: List of published messages.
    """
    def __init__(self):
        super().__init__()
        self.log = []

    def publish(self, message):
        self.log.append(message)
        super().publish(message)

    def reset(self):
        """Reset log."""
        self.log = []
