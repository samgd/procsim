from procsim.feedable import Feedable

class WriteUnitStub(Feedable):
    """Stub to receive IntegerUnit Results from.

    Attributes:
        result: Result set on feed. (default None)
    """
    def __init__(self):
        self.result = None

    def feed(self, result):
        self.result = result

    def busy(self):
        return False
