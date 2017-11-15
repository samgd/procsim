class BroadcastBus:
    """BroadcastBus coordinates publishing a message to all subscribers.

    A subscriber must have a `receive' method that takes one argument.
    """

    def __init__(self):
        self.subscribers = set()

    def subscribe(self, component):
        """Subscribe a component so that it receives published messages.

        Args:
            component: Component to subscribe to the BroadcastBus.
        """
        self.subscribers.add(component)

    def publish(self, message):
        """Publish message to all subscribed components.

        Calls the receive method of each component passing message as the only
        argument.

        Args:
            message: Message that all subscribed components will receive.

        Raises:
            AttributeError if a subscribed component does not have a receive
            method.
        """
        for subscriber in self.subscribers:
            subscriber.receive(message)
