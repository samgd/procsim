from procsim.clocked import Clocked
from procsim.feedable import Feedable

class PipelineStage(Clocked, Feedable):
    """Abstract class representing a single stage in the pipeline."""

    def __init__(self):
        super().__init__()
