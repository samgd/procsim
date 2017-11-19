from procsim.feedable import Feedable

class FeedLog(Feedable):
    """FeedLog logs all values fed to it and is never full.

    Attributes:
        log: List of fed food.
    """
    def __init__(self):
        self.log = []

    def feed(self, food):
        self.log.append(food)

    def full(self):
        return False

    def reset(self):
        self.log = []
