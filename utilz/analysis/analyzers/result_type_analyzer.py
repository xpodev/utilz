from functools import singledispatchmethod

from utilz.analysis.code_analyzer import Analyzer, CodeAnalysisResult, AnalyzerResult
from miniz.core import TypeProtocol, ObjectProtocol
from miniz.interfaces.signature import IParameter
from miniz.type_system import Void
from miniz.vm import instructions as vm
from miniz.vm.type_stack import TypeStack


class Result(AnalyzerResult["ResultTypeAnalyzer"]):
    result_type: TypeProtocol

    def __init__(self, analyzer, result_type):
        super().__init__(analyzer)
        self.result_type = result_type


class ResultTypeAnalyzer(Analyzer):
    _stack: TypeStack | None

    def __init__(self):
        self.reset()

    def analyze(self, result: CodeAnalysisResult) -> Result:
        for instruction in result.code:
            self._apply(instruction)

        return Result(self, self._stack.top(default=Void))

    def reset(self):
        self._stack = TypeStack()

    @classmethod
    def quick_analysis(cls, code: list[vm.Instruction], context: dict[IParameter, ObjectProtocol], *_, **__) -> Result:
        return cls().analyze(CodeAnalysisResult(code=code, context=context, additional_information=None))

    @singledispatchmethod
    def _apply(self, inst: vm.Instruction):
        raise NotImplementedError(f"{type(inst).__name__}")

    @_apply.register
    def _(self, inst: vm.Call):
        self._stack.apply_signature(inst.callee.signature)

    @_apply.register
    def _(self, inst: vm.CreateInstance):
        self._stack.push_type(inst.constructor.owner)

    @_apply.register
    def _(self, inst: vm.LoadArgument):
        self._stack.push_argument(inst.parameter)

    @_apply.register
    def _(self, inst: vm.LoadField):
        self._stack.push_field(inst.field)

    @_apply.register
    def _(self, inst: vm.LoadLocal):
        self._stack.push_local(inst.local)

    @_apply.register
    def _(self, inst: vm.LoadObject):
        self._stack.push_object(inst.object)


