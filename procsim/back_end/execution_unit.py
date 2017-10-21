import abc

from procsim.pipeline_stage import PipelineStage

class ExecutionUnit(PipelineStage):
    """Abstract class representing a single ExecutionUnit."""

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def capability(self):
        """Return the class of Instructions that can be executed by this unit.

        Returns:
            Instruction class.
        """
        pass
