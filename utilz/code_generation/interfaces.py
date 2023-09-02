from dataclasses import dataclass
from typing import Any

from miniz.core import ObjectProtocol
from miniz.vm.instructions import ICallInstruction
from utilz.code_generation.core import CodeGenerationResult


@dataclass(slots=True)
class BoundMemberCode(CodeGenerationResult):
    member: ObjectProtocol

    @property
    def instance(self):
        return self.code


class CallSiteCode(CodeGenerationResult):
    @property
    def call_instruction(self) -> ICallInstruction | Any:
        return self.code[-1]

    @call_instruction.setter
    def call_instruction(self, value):
        self.code[-1] = value

    @property
    def callee(self):
        return self.call_instruction.callee

    @callee.setter
    def callee(self, value):
        self.call_instruction.callee = value
