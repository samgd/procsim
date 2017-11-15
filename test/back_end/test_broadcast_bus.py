import random
import unittest

from procsim.back_end import broadcast_bus

class TestBroadcastBus(unittest.TestCase):

    def test_broadcast_bus_valid(self):
        """Ensure all messages received by subscribers."""

        message_pool = ['foo', 'bar', 'baz', 'bang',
                        1, 2, 3, 4, 5,
                        [], {}, set(),
                        [1], {'a': 0}, set(['a'])]

        for _ in range(100):
            bus = broadcast_bus.BroadcastBus()

            # Generate a random number of subscribers.
            subscribers = []
            for _ in range(random.randint(0, 100)):
                subscriber = SubscriberStub()
                subscribers.append(subscriber)
                bus.subscribe(subscriber)

            # Generate and publish random messages from message pool.
            messages = []
            for _ in range(random.randint(0, 50)):
                message = random.choice(message_pool)
                messages.append(message)
                bus.publish(message)

            # Check all messages received by all subscribes.
            for subscriber in subscribers:
                self.assertListEqual(subscriber.messages, messages)

            # Ensure new subscribers receive published messages.
            new = SubscriberStub()
            bus.subscribe(new)
            message = random.choice(message_pool)
            bus.publish(message)
            self.assertListEqual(new.messages, [message])

    def test_broadcast_bus_invalid(self):
        """Ensure exception raised for invalid subscriber."""
        bus = broadcast_bus.BroadcastBus()
        bus.subscribe('foobar')
        with self.assertRaises(AttributeError):
            bus.publish('test')

class SubscriberStub:
    def __init__(self):
        self.messages = []

    def receive(self, message):
        self.messages.append(message)
