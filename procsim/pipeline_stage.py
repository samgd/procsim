from procsim.clocked import Clocked
from procsim.feedable import Feedable
from procsim.flushable import Flushable

class PipelineStage(Clocked, Feedable, Flushable):
    """Abstract class representing a single stage in the pipeline."""

    def __init__(self):
        super().__init__()
