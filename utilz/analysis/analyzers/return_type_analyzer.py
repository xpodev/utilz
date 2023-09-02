from functools import singledispatchmethod

from utilz.analysis.analyzers import ResultTypeAnalyzer
from utilz.analysis.code_analyzer import Analyzer, CodeAnalysisResult, AnalyzerResult, CodeAnalyzer
from miniz.core import TypeProtocol, ObjectProtocol
from miniz.interfaces.signature import IParameter
from miniz.type_system import Void
from miniz.vm import instructions as vm
from miniz.vm.type_stack import TypeStack


class Result(AnalyzerResult["ReturnTypeAnalyzer"]):
    possible_return_types: list[TypeProtocol]

    def __init__(self, analyzer, possible_return_types):
        super().__init__(analyzer)
        self.possible_return_types = possible_return_types


class ReturnTypeAnalyzer(Analyzer):
    _paths: list[list[vm.Instruction]]

    def __init__(self):
        self.reset()

    def analyze(self, result: CodeAnalysisResult) -> Result:
        self._calculate_paths(result.code)

        types = []
        for path in self._paths:
            types.append(ResultTypeAnalyzer.quick_analysis(path, result.context).result_type)

        return Result(self, types)

    def reset(self):
        self._paths = []

    @classmethod
    def quick_analysis(cls, code: list[vm.Instruction], context: dict[IParameter, ObjectProtocol], *_, **__) -> Result:
        return cls().analyze(CodeAnalysisResult(code=code, context=context, additional_information=None))

    def _calculate_paths(self, code: list[vm.Instruction]):
        path = []
        for inst in code:
            if isinstance(inst, vm.Return):
                self._paths.append(path)
                path = []
            else:
                path.append(inst)
