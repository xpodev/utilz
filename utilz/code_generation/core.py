from dataclasses import dataclass

from miniz.vm.instruction import Instruction


@dataclass(slots=True)
class CodeGenerationResult:
    code: list[Instruction]
