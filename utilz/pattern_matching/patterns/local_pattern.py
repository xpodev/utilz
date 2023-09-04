from miniz.concrete.function import Local
from utilz.analysis.analyzers import ResultTypeAnalyzer
from utilz.code_generation.core import CodeGenerationResult
from utilz.pattern_matching import IPattern, BasicMatchResult
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm


class LocalPattern(IPattern):
    _local: Local

    def __init__(self, local: Local):
        self._local = local

    @property
    def local(self):
        return self._local

    def match(self, source: CodeGenerationResult, **_) -> BasicMatchResult | None:
        source_type = ResultTypeAnalyzer.quick_analysis(source.code, {}).result_type
        if not assignable_to(source_type, self.local.type):
            return None
        return BasicMatchResult(self, source, [*source.code, vm.SetLocal(self.local)])
