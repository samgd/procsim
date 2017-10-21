from procsim.feedable import Feedable

class DecodeStub(Feedable):
    """Stub to receive Fetched instructions from.

    Attributes:
        log: List of fed instruction strings.
    """
    def __init__(self):
        self.log = []

    def feed(self, instruction_str):
        self.log.append(instruction_str)

    def busy(self):
        return False
