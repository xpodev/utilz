from dataclasses import dataclass

from miniz.core import TypeProtocol
from miniz.vm.instruction import Instruction


class IMatchResult:
    """
    Contains information on the source type, the target and the code which will move the data from
    the source object into the target when executed.
    """

    source: TypeProtocol
    target: "IPattern"
    code: list[Instruction]


class BasicMatchResult(IMatchResult):
    def __init__(self, target: "IPattern", source: TypeProtocol, code: list[Instruction]):
        self.source = source
        self.target = target
        self.code = code


@dataclass(slots=True, frozen=True)
class PatternOptions:
    include_source_code: bool = False
    include_source_node: bool = False
    source_code_parameter: str = "source_code"
    source_node_parameter: str = "source_node"


class IPattern:
    options = PatternOptions()

    def match(self, source: TypeProtocol, **kwargs) -> IMatchResult | None:
        """
        Try to match the source type into this (self) pattern and return the result object.
        This function generates code with the assumption that the matched object is on the
        top of the stack.

        :param source: The source type which should be matched against.
        :return: An `IMatchResult` object if the match was successful, `None` otherwise.
        """
        raise NotImplementedError
