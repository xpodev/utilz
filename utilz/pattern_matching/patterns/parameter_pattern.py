from miniz.concrete.function import Parameter
from utilz.analysis.analyzers import ResultTypeAnalyzer
from utilz.code_generation.core import CodeGenerationResult
from utilz.pattern_matching import IPattern, BasicMatchResult
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm


class ParameterPattern(IPattern):
    _parameter: Parameter

    def __init__(self, local: Parameter):
        self._parameter = local

    @property
    def parameter(self):
        return self._parameter

    def match(self, source: CodeGenerationResult, **_) -> BasicMatchResult | None:
        source_type = ResultTypeAnalyzer.quick_analysis(source.code, {}).result_type
        if not assignable_to(source_type, self.parameter.parameter_type):
            return None
        return BasicMatchResult(self, source, [*source.code, vm.SetArgument(self.parameter)])
