from miniz.vm.instruction import Instruction
from utilz.debug.file_info import Span, DocumentInfo


class SequencePoint:
    instruction: Instruction
    span: Span
    document: DocumentInfo
