from typing import TypeVar, Generic

from miniz.interfaces.function import IFunctionBody
from miniz.vm.instruction import Instruction
from utilz.algorithms import binary_search
from utilz.debug.file_info import DocumentInfo, Span
from utilz.debug.sequence_point import SequencePoint

_T = TypeVar("_T")


class DebugInformation(Generic[_T]):
    definition: _T
    document: DocumentInfo


class FunctionBodyDebugInformation(DebugInformation[IFunctionBody]):
    def __init__(self, body: IFunctionBody, document: DocumentInfo):
        self.definition = body
        self.document = document
        self.sequence_points = []

    def add_sequence_point(self, inst: Instruction, span: Span):
        point = SequencePoint()
        point.document = self.document
        point.instruction = inst
        point.span = span
        self.sequence_points.insert(binary_search.find_index(self.sequence_points, inst.index, lambda p: p.instruction.index), point)
