from functools import singledispatchmethod

from miniz.vm.runtime import Interpreter
from utilz.analysis.code_analyzer import Analyzer, CodeAnalysisResult, AnalyzerResult
from miniz.core import ObjectProtocol
from miniz.interfaces.signature import IParameter
from miniz.vm import instructions as vm


class Result(AnalyzerResult["CompilerTimeExpressionAnalyzer"]):
    result_value: ObjectProtocol | None

    def __init__(self, analyzer, result_value: ObjectProtocol):
        super().__init__(analyzer)
        self.result_value = result_value

    @property
    def result_type(self):
        return self.result_value.runtime_type

    @property
    def has_result(self):
        return self.result_value is not None


class CompileTimeExpressionAnalyzer(Analyzer):
    _vm: Interpreter

    def __init__(self):
        self.reset()

    def analyze(self, result: CodeAnalysisResult) -> Result:
        ctx = self._vm.run(result.code)
        return Result(self, ctx.top())

    def reset(self):
        ...

    @classmethod
    def quick_analysis(cls, code: list[vm.Instruction], context: dict[IParameter, ObjectProtocol], *_, **__) -> Result:
        return cls().analyze(CodeAnalysisResult(code=code, context=context, additional_information=None))
